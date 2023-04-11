lib:
    {
        network-manager-cli config:
        sudo apt-get install network-manager (Normally -> Already have on DWS machine)

        UI_tkinter:
        sudo apt install python3-tk
        
        wifi config:
        wifi_default_name = Ninja Van -> Usually in Viet Nam
        wifi_4g = dws4g -> SET name in phone or wifi's name transmitter
        wifi_pass = Ninjav@nwifi! -> All device set 1 key password

        git config:
        sudo apt install git
        git clone <http>
        
        speedtest-cli config:
        sudo apt install speedtest-cli ; apt update;\
        sudo gzip -k9 /usr/lib/python3/dist-packages/speedtest.py; \
        sudo wget https://raw.githubusercontent.com/sivel/speedtest-cli/v2.1.3/speedtest.py -O /usr/lib/python3/dist-packages/speedtest.py
    }