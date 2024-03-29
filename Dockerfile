FROM python:3-alpine

RUN apk add --no-cache restic

WORKDIR /app

COPY cron_backup.sh /etc/periodic/daily/backup

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["/app/entrypoint.sh"]