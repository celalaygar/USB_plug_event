#!/bin/bash

echo "Running ytstart.sh" >> /tmp/yt_debug.log
source /opt/venv/bin/activate  # Activate the virtual environment
python3 /home/skyflower/scripts/yt.py >> /tmp/yt_debug.log 2>&1
deactivate  # Deactivate the virtual environment
echo "Finished ytstart.sh" >> /tmp/yt_debug.log
