from tkinter import Tk, Frame, Menu
from Functions import *

class GUI_Menu():
    def __init__(self, root, Devices, Buttons):
        self.root = root
        self.Devices = Devices
        self.Buttons = Buttons
        # create a menubar
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)
    
    def Call_Menu(self):
        self.File_Menu()
        self.Device_Menu()
        self.Help_Menu()
        
    def File_Menu(self):
        # create the file_menu
        file_menu = Menu(
            self.menubar,
            tearoff=0
        )
        
        # add menu items to the File menu
        file_menu.add_command(label='New')
        file_menu.add_command(label='Open...')
        file_menu.add_command(label='Close')
        file_menu.add_separator()

        # add Exit menu item
        file_menu.add_command(
            label='Exit',
            command=self.root.destroy
        )
        
        # add the File menu to the menubar
        self.menubar.add_cascade(
            label="File",
            menu=file_menu
        )
    
    def Device_Menu(self):
        device_menu = Menu(
            self.menubar,
            tearoff=0
        )
        
        device_menu.add_command(label = 'Add New Device', command =lambda: Discover_Devices(self.root, self.Devices, self.Buttons))
        device_menu.add_command(label = 'Send Message', command =lambda: send_message(self.Devices))
        device_menu.add_command(label = 'Remove Device', command =lambda: Remove_Devices(self.root, self.Devices, self.Buttons))
        
        self.menubar.add_cascade(
            label="Device",
            menu=device_menu
        )
        
    def Help_Menu(self):
        # create the Help menu
        help_menu = Menu(
            self.menubar,
            tearoff=0
        )

        help_menu.add_command(label='Welcome')
        help_menu.add_command(label='About...')

        # add the Help menu to the menubar
        self.menubar.add_cascade(
            label="Help",
            menu=help_menu
        )