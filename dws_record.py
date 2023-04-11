#!/usr/bin/env python
import subprocess
import time
import threading

from tkinter import *

import datetime
import psutil
import os
import signal

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
    # Init Time to check back internet
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
get_speed = '0.000'
LAN_to_wifi = False
wifi_driver = True
wifi_connecting = False
####################################################################################


def oen_dws():
    try:
        p = subprocess.Popen(["ninjavan"])
    except:
        print("execute ninjavan err")


def close_dws():
    try:
        for pid in (process.pid for process in psutil.process_iter() if process.name() == "electron"):
            os.kill(pid, signal.SIGTERM)
            for pid in (process.pid for process in psutil.process_iter() if process.name() == "ninjavan"):
                os.kill(pid, signal.SIGTERM)
        for pid in (process.pid for process in psutil.process_iter() if process.name() == "node"):
            os.kill(pid, signal.SIGTERM)
    except Exception as e:
        print("close ninjavan err: " + str(datetime.datetime.now()) + ' ', e)


def enet_mes_UI(data, sta):
    global enet_ui
    enet_ui = Tk()
    enet_ui.title('Message from DWS Record')
    enet_ui.geometry("775x140+100+200")
    if ('Connecting' in data):
        enet_ui.configure(background='yellow')
        mes_txt = Label(enet_ui, text=data, font=(
            'Arial Black', 30), background='yellow')
    else:
        if (sta):
            enet_ui.configure(background='green')
            mes_txt = Label(enet_ui, text=data, font=(
                'Arial Black', 30), background='green')
        else:
            enet_ui.configure(background='red')
            mes_txt = Label(enet_ui, text=data, font=(
                'Arial Black', 60), background='red')
    mes_txt.pack(fill='both', expand=True)
    enet_ui.after(3000, lambda: enet_ui.destroy())
    enet_ui.mainloop()


def memory_mes_UI(data):
    global memory_ui
    memory_ui = Tk()
    memory_ui.title('Message from DWS Record')
    memory_ui.attributes('-fullscreen', True)
    memory_ui.configure(background='red')
    mes_ui_1 = Label(memory_ui, text=data, font=(
        'Arial Black', 100), background='red')
    mes_ui_1.pack()
    mes_ui_3 = Label(memory_ui, text="               ", font=(
        'Arial Black', 200, "bold"), background='red')
    mes_ui_3.pack()
    mes_ui_2 = Label(memory_ui, text="Refreshing Data", font=(
        'Arial Black', 150, "bold"), background='red')
    mes_ui_2.pack()

    memory_ui.after(60000, lambda: memory_ui.destroy())
    memory_ui.mainloop()


def resfresh_wifi():
    subprocess.run("nmcli radio wifi off",
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    time.sleep(2)
    subprocess.run("nmcli radio wifi on",
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    time.sleep(10)


def verify_wifi_sta():
    global LAN_to_wifi, wifi_connecting
    time.sleep(15)
    ver_wifi = subprocess.run(["curl", "-I", "https://linuxhint.com/"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=1.5)
    ver_wifi_mes = ver_wifi.stdout.decode(encoding='utf-8')
    if (ver_wifi_mes == ''):
        raise Exception
    LAN_to_wifi = True
    wifi_connecting = False


def verify_interrupt_sta():
    global wifi_connecting
    time.sleep(3)
    try:
        ver_net = subprocess.run(["curl", "-I", "https://linuxhint.com/"],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=2)
        ver_net_mes = ver_net.stdout.decode(encoding='utf-8')
        if (ver_net_mes == ''):
            raise Exception
    except Exception:
        wifi_connecting = True
        enet_mes_UI(
            'Connecting to Wifi, Please wait', True)


def memory_mes_UI(data):
    global memory_ui
    memory_ui = Tk()
    memory_ui.title('Message from DWS Record')
    memory_ui.attributes('-fullscreen', True)
    memory_ui.configure(background='red')
    mes_ui_4 = Label(memory_ui, text="               ", font=(
        'Arial Black', 30, "bold"), background='red')
    mes_ui_4.pack()
    mes_ui_1 = Label(memory_ui, text=data, font=(
        'Arial Black', 100), background='red')
    mes_ui_1.pack()
    mes_ui_3 = Label(memory_ui, text="               ", font=(
        'Arial Black', 175, "bold"), background='red')
    mes_ui_3.pack()
    mes_ui_2 = Label(memory_ui, text="Clear Image 1st!", font=(
        'Arial Black', 150, "bold"), background='red')
    mes_ui_2.place(relx=0.5, rely=0.5, anchor=CENTER)
    mes_ui_2.pack()

    memory_ui.after(60000, lambda: memory_ui.destroy())
    memory_ui.mainloop()


def get_speed_net():
    global get_speed, LAN_to_wifi, wifi_driver, net_sta, \
        init_timer_enet, wifi_pass, wifi_default_name, wifi_4g_name, wifi_connecting
    while (True):
        try:
            check_net = subprocess.run(["curl", "-I", "https://linuxhint.com/"],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=3)
            check_net_mes = check_net.stdout.decode(encoding='utf-8')
            if not ('HTTP/2 200' in check_net_mes):
                raise Exception
            try:
                response_speed = subprocess.Popen(
                    '/usr/bin/speedtest', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
                index_fst = response_speed.find('Download: ')
                index_ser = response_speed.find('Mbit/s')
                get_speed = response_speed[index_fst +
                                           9:index_ser-1].strip()
                get_speed_con = float(get_speed)
            except:
                raise Exception

            if (LAN_to_wifi == True) and (get_speed_con >= 70):
                subprocess.run("nmcli radio wifi off",
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                LAN_to_wifi = False
                time.sleep(10)
                enet_mes_UI('LAN network is Back', True)
            print('Internet is good: Speed ' +
                  str(get_speed) + 'Mbit/s')
            time.sleep(init_timer_enet)
        except Exception:
            verify_interrupt_sta()
            time.sleep(1)
            if wifi_connecting:
                password = r'{}'.format(wifi_pass)
                try:
                    resfresh_wifi()
                    output = subprocess.check_output(
                        ['nmcli d wifi connect "{wifi_default_name}" password "{password}"'.format(
                            wifi_default_name=wifi_default_name, password=password)],
                        shell=True
                    ).decode('utf-8')
                    verify_wifi_sta()
                    enet_mes_UI('NinjaVan Wifi has connected', True)
                except Exception:
                    try:
                        resfresh_wifi()
                        output_4g = subprocess.check_output(
                            ['nmcli d wifi connect "{wifi_4g_name}" password "{password}"'.format(
                                wifi_4g_name=wifi_4g_name, password=password)],
                            shell=True
                        ).decode('utf-8')
                        verify_wifi_sta()
                        enet_mes_UI('4G Wifi has connected', True)
                    except Exception:
                        enet_mes_UI('Network is Crash', False)


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
            # print('Disk in Alarm')
            memory_mes_UI('Disk in Alarm')
        else:
            print('Still able in using (Free in use: ' + available_space + ')')
        time.sleep(init_timer_space)


thread_check_speed_net = threading.Thread(target=get_speed_net)
thread_check_speed_net.start()

thread_Alarm_free_space = threading.Thread(target=Alarm_free_space)
thread_Alarm_free_space.start()
