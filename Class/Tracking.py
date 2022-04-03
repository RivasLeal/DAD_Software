import csv

###################################################################################################################################################
###################################################################################################################################################
################################################ Is Keeping Track of the overall system, ##########################################################
################################################ Because Buttons don't have any way of ############################################################
################################################ returning back any information ###################################################################
###################################################################################################################################################
###################################################################################################################################################

#Current Devices
class Current_devices:
    def __init__(self, devices = list(),BLU_dev = list(), num =-1, xpos = 0,ypos = 450):
        #Saves a list of devices and their class connection
        self.devices = devices
        self.BLU_dev = BLU_dev
        
        #Keeps track of the number of devices
        self.num = num
        
        #Keeps track of the current xpos and ypos
        self.xpos = xpos
        self.ypos = ypos
        
    def update_ypos(self,update_pos = 100):
        #Updates ypos
        self.ypos = self.ypos + update_pos
    
    def update_xpos(self,update_pos = 125):
        #Updates xpos
        self.xpos = self.xpos + update_pos
        
        #If xpos is above a certain threshold
        if(self.xpos > 500):
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
    
    #Removes the device from a specified location and closes the connection
    def remove_device(self, pos):
        self.devices.pop(pos)
        self.BLU_dev[pos].CloseConnection()
        self.BLU_dev.pop(pos)
        self.num = self.num - 1

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
    
    def update_name(self,name):
        self.name = name
        
    def save_directory(self, name):
        self.directory = name
        
    def save_file(self):
        self.loc = self.directory  + '/'+ self.name
        #Creates the csv at a predetermine location
        
        file = open(self.loc, 'w')
        writer = csv.writer(file)
        #This will be a switch statement depending on the sensor types
        row = ['Time','Device_Name' , 'Data']
        writer.writerow(row)
        file.close()
        
