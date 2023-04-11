from tkinter import *
import threading
import time
def enet_mes_UI():
    global enet_ui,data
    enet_ui = Tk()
    enet_ui.resizable(0,0)
    enet_ui.title('Message from DWS Record')
    enet_ui.geometry("825x140+0+140")
    #enet_ui.configure(background='red')
    # mes_txt = Label(enet_ui, text='Network is crash', font=(
    #     'Arial Black', 70), background='red')
    enet_ui.configure(background='green')
    mes_txt = Label(enet_ui, text='Internet is Back, Please wait 2 minutes', font=(
        'Arial Black', 30), background='green')
    mes_txt.pack(fill='both', expand=True)
    enet_ui.lift()
    enet_ui.attributes("-topmost", True)
    enet_ui.after(5000, lambda: enet_ui.destroy())
    enet_ui.mainloop()


def memory_mes_UI():
    memory_ui = Tk()
    memory_ui.title('Message from DWS Record')
    memory_ui.geometry("825x140+0+140")
    memory_ui.configure(background='red')
    mes_ui = Label(memory_ui, text='Memory is LOW', font=(
        'Arial Black', 70), background='red')
    mes_ui.pack()
    memory_ui.lift()
    memory_ui.attributes("-topmost", True)
    memory_ui.after(5000, lambda: memory_ui.destroy())
    memory_ui.mainloop()

print('Start program')
time.sleep(10)
enet_mes_UI()
