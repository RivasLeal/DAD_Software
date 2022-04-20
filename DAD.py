from tkinter import *
import sys
import os
import asyncio
import PIL
from PIL import ImageTk
sys.path.append(os.path.abspath("Class"))
from Bluetooth_Devices import *
from File_Menu import *
from Tracking import *
from Functions import *
from Graphing import *
from Display_Window import *

def main():
    #Creates the Main Gui
    root = Tk()
    
    #Title for the Gui
    root.title('DAD')
    
    #General Configuration
    root.configure(background = 'light gray')
    
    #Setting the Size
    root.geometry("820x790")
    
    #Taskbar Icon for the GUI
    image = PIL.Image.open("dad.png")
    resize_image = image.resize((500,400))
    photo = PhotoImage(file = "dad.png")
    root.iconphoto(True, photo)
    
    #Is being used to store a filename and directory for recording purposes
    FileName = Current_File()
    
    #Is being used to keep track of the the number of devices and type
    Devices = Current_devices(root = root)
    Devices.ADDFile(FileName)
    
    #Is being used to keep track of each button per device
    Buttons = Current_Buttons()
    
    #Make a Data Display Window
    Display = DisplayWindow(root)
    
    #Makes a plot
    img = ImageTk.PhotoImage(resize_image)
    label1 = Label(image=img)
    label1.image = img

    # Position image
    label1.place(x=0, y=0)
    #make_plot = Plotting_EMG(root,500,400)
    
    #Makes sure that the rest of the software has access to devices, buttons and filenames
    Task_bar = GUI_Menu(root, Devices, Buttons, FileName, Display)
    
    #Creates the taskbar
    Task_bar.Call_Menu()
    
    root.protocol("WM_DELETE_WINDOW", Devices.ClOSING)
    
    #Runs the Gui
    root.mainloop()

if __name__ == '__main__':
    #Runs the DAD software
    main()