FROM --platform=$BUILDPLATFORM python:3-alpine AS build

RUN apk add --no-cache restic

WORKDIR /app

COPY start_backup.sh /etc/periodic/daily/backup

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["python", "code.py"]