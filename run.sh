#!/bin/bash
gnome-terminal --working-directory=/home/admin1/Desktop/record/ -x bash -c "sudo apt install speedtest-cli;sleep 2;apt update; \
    gzip -k9 /usr/lib/python3/dist-packages/speedtest.py;sleep 2; \
    wget https://raw.githubusercontent.com/sivel/speedtest-cli/v2.1.3/speedtest.py -O /usr/lib/python3/dist-packages/speedtest.py"