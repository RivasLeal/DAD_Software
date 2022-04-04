import csv
from tkinter import *
from datetime import datetime

###################################################################################################################################################
###################################################################################################################################################
################################################ Is Keeping Track of the overall system, ##########################################################
################################################ Because Buttons don't have any way of ############################################################
################################################ returning back any information ###################################################################
###################################################################################################################################################
###################################################################################################################################################

#Current Devices
class Current_devices:
    def __init__(self,root, devices = list(),BLU_dev = list(), num =-1, xpos = 0,ypos = 450):
        #Saves a list of devices and their class connection
        self.devices = devices
        self.BLU_dev = BLU_dev
        
        self.root = root
        
        #Keeps track of the number of devices
        self.num = num
        
        #Keeps track of the current xpos and ypos
        self.xpos = xpos
        self.ypos = ypos
        
        self.collection = list()
        
        self.RecordCollect = list()
        
    def ADDFile(self,file):
        self.File = file
        
    def update_ypos(self,update_pos = 100):
        #Updates ypos
        self.ypos = self.ypos + update_pos
    
    def update_xpos(self,update_pos = 125):
        #Updates xpos
        self.xpos = self.xpos + update_pos
        
        #If xpos is above a certain threshold
        if(self.xpos > 380):
            #Resets xpos to 0
            self.xpos = 0
            
            #Updates ypos
            self.update_ypos()
    
    #Adds a new device to the list  
    def new_device(self, device):
        self.devices.append(device)
        self.num = self.num + 1
    
    #Adds the Bluetooth object to the list
    def new_BLU(self, BLU):
        self.BLU_dev.append(BLU)
        return BLU
    
    #Grabs the latest device added    
    def latest_BLU(self):
        return self.BLU_dev[self.num]
    
    def AddData(self, data):
        self.collection.append(data[0])
        if self.File.Recording:
            self.RecordCollect.append(data[1])
            
    async def CollectData(self):
        while self.File.Recording:
            file = open(self.File.loc, 'a')
            if self.RecordCollect:
                writer = csv.writer(file)
                now = datetime.now()
                Ctime = now.strftime("%H:%M:%S")
                row = [Ctime, 'EKG', self.RecordCollect[0]]
                writer.writerow(row)
                self.RecordCollect.pop(0)
            file.close()
    
    #Removes the device from a specified location and closes the connection
    def remove_device(self, pos):
        self.devices.pop(pos)
        self.BLU_dev[pos].CloseConnection()
        self.BLU_dev.pop(pos)
        self.num = self.num - 1
    
    def TurnOFF(self):
        for dev in self.BLU_dev:
            dev.TURN_OFF()
            
    def ClOSING(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.File.Recording = False
            self.TurnOFF()
            self.root.destroy()

#Keeps track of devices that may be added 
class Potential_devices:
    def __init__(self, device_num, state):
        self.device_num = device_num
        self.state = False
    
    #Changes state
    def change_state(self):
        self.state = not self.state
        
#Keeps track of all the current Buttons 
class Current_Buttons:
    def __init__(self, Buttons = list()):
        #Default
        self.Buttons = Buttons
        self.counter = -1
    
    #Button is added to the list    
    def add_Button(self, Button):
        self.counter = self.counter + 1
        self.Buttons.append(Button)
    
    #Returns the latest button added
    def latest_Button(self):
        return self.Buttons[self.counter]
    
    #Removes the button from the GUI
    def remove_button(self, pos):
        self.Buttons[pos][0].destroy()
        self.Buttons[pos][1].destroy()
        self.Buttons[pos][2].destroy()
        self.Buttons.pop(pos)
        self.counter = self.counter - 1

#Keeps track of the current File and destination
class Current_File:
    def __init__(self, name = 'default'):
        self.name = name
        self.Recording = False
    
    def update_name(self,name):
        self.name = name
        
    def save_directory(self, name):
        self.directory = name
        
    def StopRecording(self):
        messagebox.showinfo("Information","Stopping Recording")
        self.Recording = False
        
    def save_file(self):
        self.loc = self.directory  + '/'+ self.name
        #Creates the csv at a predetermine location
        
        file = open(self.loc, 'w')
        writer = csv.writer(file)
        #This will be a switch statement depending on the sensor types
        row = ['Time','Device_Name' , 'Data']
        writer.writerow(row)
        file.close()