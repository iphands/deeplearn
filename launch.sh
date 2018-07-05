#!/bin/bash
set -e

make
export DISPLAY=:99

#xvfb-run -n 99 --server-args="-screen :0 300x300x24" /usr/bin/snes9x-gtk /path/to/rom
#sleep 5

PID=$(pgrep -P `ps aux | fgrep xvfb-run | fgrep 99 | awk '{print $2}'` snes)
echo "Using pid: $PID"

source deeplearnvenv/bin/activate
python src/kart.py $PID
# python src/test2.py $PID

wait %1
