#!/usr/bin/env sh

cmdLineParameter="$1"
if [ -z "$cmdLineParameter" ]; then
    exec python code.py $cmdLineParameter
    exit 0
fi
echo "Volume Backup Container Started"
printenv > /etc/environment
exec /usr/sbin/crond -f -l 2