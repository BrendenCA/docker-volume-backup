#!/usr/bin/env sh

cmdLineParameter="$1"
if [ "$cmdLineParameter" = "init" ]; then
    exec python code.py init
    exit 0
fi
echo "Volume Backup Container Started"
printenv > /etc/environment
exec /usr/sbin/crond -f -l 2