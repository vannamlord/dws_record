#!/usr/bin/env python
import subprocess
import datetime
import time
import threading
# Read status of Tool on DWS
####################################################################################
try:
    file1 = open('parameter.txt', 'r')
    dict_init = {}
    for line in file1:
        line = line.strip()
        list_line = line.split(' = ')
        dict_init[list_line[0]] = list_line[1]
    file1.close()
    # Time to check back internet
    init_timer_enet = int(dict_init['init_timer_enet'])
    init_timer_space = int(dict_init['init_timer_space'])
    init_space = int(dict_init['init_space'])
    wifi_default_name = str(dict_init['wifi_default_name'])
    wifi_4g_name = str(dict_init['wifi_4g_name'])
    wifi_pass = str(dict_init['wifi_pass'])
except:
    init_timer_enet = 180
    init_timer_space = 18000
    init_space = 10
####################################################################################

wifi_sta = False
get_speed = '0.000'
LAN_to_wifi = False
wifi_driver = True
net_sta = False


def get_speed_net():
    global get_speed, LAN_to_wifi, wifi_sta, wifi_driver, net_sta, init_timer_enet, wifi_name, wifi_pass
    while (True):
        try:
            p = subprocess.run(["curl", "-I", "https://linuxhint.com/"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=1)
            response_speed = subprocess.Popen(
                '/usr/bin/speedtest', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
            index_fst = response_speed.find('Download: ')
            index_ser = response_speed.find('Mbit/s')
            get_speed = response_speed[index_fst+9:index_ser-1].strip()
            get_speed = float(get_speed)
            if (LAN_to_wifi == True) and (get_speed >= 60):
                wifi_off = subprocess.run("nmcli radio wifi off",
                                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                LAN_to_wifi = False
                wifi_sta = False
                time.sleep(10)
            print('Internet is good: Speed '+ str(get_speed) + 'Mbit/s')
            # time.sleep(init_timer_enet)
        except Exception:
            try:
                # Turn on wifi (=> Also check driver)
                subprocess.run("nmcli radio wifi on",
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                time.sleep(5)
                # Connect to ssid and password
                password = r'{}'.format(wifi_pass)
                try:
                    output = subprocess.check_output(
                        ['nmcli d wifi connect "{wifi_default_name}" password "{password}"'.format(
                            wifi_default_name=wifi_default_name, password=password)],
                        shell=True
                    ).decode('utf-8')
                    if ('successfully activated' in output):
                        print('Ninja Van Wifi has connected')
                    time.sleep(15)
                    try:
                        subprocess.run(["curl", "-I", "https://linuxhint.com/"],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=1)
                    except:
                        try:
                            output_4g = subprocess.check_output(
                                ['nmcli d wifi connect "{wifi_4g_name}" password "{password}"'.format(
                                    wifi_4g_name=wifi_4g_name, password=password)],
                                shell=True
                            ).decode('utf-8')
                            if ('successfully activated' in output_4g):
                                print('4G Wifi has connected')
                        except:
                            print('Error in connecting with 4G')
                        time.sleep(15)
                        try:
                            subprocess.run(["curl", "-I", "https://linuxhint.com/"],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=1)
                        except:
                            print('All network is crash')
                except:
                    print('Error in connecting with Ninja Van Wifi')

                LAN_to_wifi = True
                wifi_sta = True
            except:
                print('Error in driver Wifi')


def Alarm_free_space():
    global init_timer_space, init_space
    while (True):
        p = subprocess.run(["df", "-h"],
                           stdout=subprocess.PIPE)
        respone_space = p.stdout.decode("utf-8")
        available_space = respone_space.split(
            '\n')[3].split('       ')[1].split('  ')[2]
        free_use = available_space.replace('G', '')
        free_use = float(free_use)
        if (free_use < init_space):
            print('Disk in Alarm')
        else:
            print('Still able in using (Free in use: ' + available_space + ')')
        time.sleep(init_timer_space)


thread_check_speed_net = threading.Thread(target=get_speed_net)
thread_check_speed_net.start()

thread_Alarm_free_space = threading.Thread(target=Alarm_free_space)
thread_Alarm_free_space.start()
