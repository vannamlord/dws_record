lib:
    {
        speedtest-cli: sudo apt install speedtest-cli ; apt update;\
        sudo gzip -k9 /usr/lib/python3/dist-packages/speedtest.py; \
        sudo wget https://raw.githubusercontent.com/sivel/speedtest-cli/v2.1.3/speedtest.py -O /usr/lib/python3/dist-packages/speedtest.py
    }