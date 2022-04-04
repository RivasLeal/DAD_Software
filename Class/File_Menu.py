from tkinter import Tk, Frame, Menu
from Functions import *

class GUI_Menu():
    def __init__(self, root, Devices, Buttons, FileName, Display):
        #Saves the Main Gui 
        self.root = root
        
        #Used to access the list of devices
        self.Devices = Devices
        
        #Used to access the buttons on the Main Gui
        self.Buttons = Buttons
        
        #Used to store the current file for recording purposes
        self.FileName = FileName
        
        #Used to store the Data Display
        self.Display = Display
        
        # create a menubar
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)
        
    #Main purpose is to run all the Menu calls
    def Call_Menu(self):
        self.File_Menu()
        self.Device_Menu()
        self.Help_Menu()
        
    def File_Menu(self):
        # create the file_menu
        file_menu = Menu(self.menubar,tearoff=0)
        
        # add menu items to the File menu
        file_menu.add_command(label='Start Recording',command = lambda : GrabFilePath(self.FileName, self.Devices))
        file_menu.add_command(label='Stop Recording', command = lambda : self.FileName.StopRecording())
        #file_menu.add_command(label='Close')
        file_menu.add_separator()
        file_menu.add_command(label='Exit',command=self.root.destroy)
        
        # add the File menu to the menubar
        self.menubar.add_cascade(label="File",menu=file_menu)
    
    def Device_Menu(self):
        #Create the Device Menu
        device_menu = Menu(self.menubar,tearoff=0)
        
        # add menu items to the Device menu
        device_menu.add_command(label = 'Add New Device', command =lambda: Discovery(self.root, self.Devices, self.Buttons, self.Display))
        device_menu.add_command(label = 'Send Message', command =lambda: send_message(self.Devices))
        device_menu.add_command(label = 'Remove Device', command =lambda: DeviceRemoval(self.root, self.Devices, self.Buttons))
        
        # add the Device menu to the menubar
        self.menubar.add_cascade(label="Device",menu=device_menu)
        
    def Help_Menu(self):
        # create the Help menu
        help_menu = Menu(self.menubar,tearoff=0)

        help_menu.add_command(label='Welcome')
        help_menu.add_command(label='About...')

        # add the Help menu to the menubar
        self.menubar.add_cascade(label="Help",menu=help_menu)