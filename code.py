import sys
import utils
import logging

VOLUME_BASE_PATH = '/data/'
ENV_FILE_PATH = '/.env'

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

if __name__ == "__main__":
    containers_array = []
    if not utils.checkEnv():
        logging.error("Environment variables not set")
        sys.exit(1)
    if(len(sys.argv) > 1 and sys.argv[1] == 'init'):
        logging.info("Initializing repo")
        utils.init_repo()
        sys.exit(0)
    with open("/config/backup.yml", "r") as stream:
        logging.info("Reading config file")
        containers_array = utils.parseConfig(stream)
    logging.info("Starting backup")
    logging.info("Backing up env file")
    utils.backup_volume(ENV_FILE_PATH)
    for container in containers_array:
        logging.info("Working on container: " + container.container_name + ", volume: " + VOLUME_BASE_PATH + container.volume_path + ", shutdown required: " + str(container.shutdown_required))
        current_container_status = False
        if container.shutdown_required:
            current_container_status = utils.is_container_running(container.container_name)
            logging.debug("Container status: " + str(current_container_status))
            if current_container_status:
                logging.info("Shutting down container: " + container.container_name)
                utils.stop_container(container.container_name)
        logging.info("Backing up container: " + container.container_name + ", volume: " + VOLUME_BASE_PATH + container.volume_path)
        utils.backup_volume(VOLUME_BASE_PATH + container.volume_path)
        if container.shutdown_required and current_container_status:
            logging.info("Starting up container: " + container.container_name)
            utils.start_container(container.container_name)