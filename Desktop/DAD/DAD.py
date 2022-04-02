from tkinter import *
import sys
import os
import asyncio
sys.path.append(os.path.abspath("Class"))
from Bluetooth_Devices import *
from File_Menu import *
from Tracking import *
from Functions import *
from Graphing import *

def main(async_loop):
    root = Tk()
    root.title('DAD')
    root.configure(background = 'light gray')
    #root.geometry("605x450")
    root.geometry("800x800")
    photo = PhotoImage(file = "dad.png")
    root.iconphoto(True, photo)
    
    Devices = Current_devices()
    Buttons = Current_Buttons()
    
    Task_bar = GUI_Menu(root, Devices, Buttons)
    Task_bar.Call_Menu()
    
    make_plot = Plotting_EMG(root,500,400)
    
    #Devices = Current_devices()
    
    #Button(master=root, text='Send Message', command= lambda: send_message(Devices)).place(x =600, y= 0)
    #root.protocol("WM_DELETE_WINDOW", )
    root.mainloop()

if __name__ == '__main__':
    async_loop = asyncio.get_event_loop()
    main(async_loop)