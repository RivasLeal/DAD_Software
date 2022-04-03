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

def main():
    #Creates the Main Gui
    root = Tk()
    
    #Title for the Gui
    root.title('DAD')
    
    #General Configuration
    root.configure(background = 'light gray')
    
    #Setting the Size
    root.geometry("800x800")
    
    #Taskbar Icon for the GUI
    photo = PhotoImage(file = "dad.png")
    root.iconphoto(True, photo)
    
    #Is being used to keep track of the the number of devices and type
    Devices = Current_devices()
    
    #Is being used to keep track of each button per device
    Buttons = Current_Buttons()
    
    #Is being used to store a filename and directory for recording purposes
    FileName = Current_File()
    
    #Makes sure that the rest of the software has access to devices, buttons and filenames
    Task_bar = GUI_Menu(root, Devices, Buttons, FileName)
    
    #Creates the taskbar
    Task_bar.Call_Menu()
    
    #Makes a plot
    make_plot = Plotting_EMG(root,500,400)
    
    #Runs the Gui
    root.mainloop()

if __name__ == '__main__':
    #Runs the DAD software
    main()