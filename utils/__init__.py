import os
import subprocess
from typing import List
import docker
import yaml

restic_env_variables=["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "RESTIC_REPOSITORY", "RESTIC_PASSWORD", "RESTIC_CACHE_DIR", "RESTIC_HOST"]
restic_env_object = {}
restic_host = ''
docker_socket = "unix://var/run/docker.sock"
docker_client = docker.DockerClient(docker_socket)

class backupConfig:
    def __init__(self, container_name: str, volume_path: str, shutdown_required: bool):
        self.container_name = container_name
        self.volume_path = volume_path
        self.shutdown_required = shutdown_required

    @classmethod
    def parseYaml(cls, containerConfig: dict) -> 'backupConfig':
        return backupConfig(containerConfig['container_name'], containerConfig['volume_path'], containerConfig['shutdown_required'])

def checkEnv() -> bool:
    myenv = os.environ
    for env in restic_env_variables:
        if myenv.get(env, '') == '':
            return False
    global restic_env_object, restic_host
    restic_env_object = {k: myenv.get(k, '') for k in restic_env_variables}
    restic_host = restic_env_object["RESTIC_HOST"]
    return True

def parseConfig(stream: str) -> List[backupConfig]:
    loaded_data = yaml.safe_load(stream)
    container_array = []
    for container in loaded_data:
        container_array.append(backupConfig.parseYaml(container))
    return container_array

def is_container_running(container_name: str) -> bool:
    try:
        container = docker_client.containers.get(container_name)
        return container.attrs["State"]["Running"]
    except docker.errors.NotFound as exc:
        print(f"Container doesn't exist\n{exc.explanation}")
    return False

def stop_container(container_name: str) -> None:
    try:
        container = docker_client.containers.get(container_name)
        container.stop()
    except docker.errors.NotFound as exc:
        print(f"Container doesn't exist\n{exc.explanation}")

def start_container(container_name: str) -> None:
    try:
        container = docker_client.containers.get(container_name)
        container.start()
    except docker.errors.NotFound as exc:
        print(f"Container doesn't exist\n{exc.explanation}")

def forget_old_snapshots() -> None:
    subprocess.run(["restic", "forget", "--keep-daily", "7", "--keep-weekly", "5", "--keep-monthly", "12", "--keep-yearly", "75", "--prune"], env = restic_env_object)

def backup_volume(volume_path: str) -> None:
    subprocess.run(["restic", "--host", restic_host, "backup", volume_path], env = restic_env_object)

def restore_volume(volume_path: str) -> None:
    subprocess.run(["restic", "restore", "latest", "--host", restic_host, "--target", "/", "--path", volume_path], env = restic_env_object)

def init_repo() -> None:
    subprocess.run(["restic", "init"], env = restic_env_object)