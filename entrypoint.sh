#!/usr/bin/env sh

echo "Volume Backup Container Started"
printenv > /etc/environment
exec /usr/sbin/crond -f -l 2