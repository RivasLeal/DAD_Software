import asyncio
import threading
import tkinter as tk
import matplotlib.animation as animation
from tkinter import *
from tkinter import filedialog as fd
from Tracking import *
from Bluetooth_Devices import *

#Makes sure that the thread runs the function to completion
def _asyncio_thread(async_loop,func):
    async_loop.run_until_complete(func)
    
def Main_DisplayData(root, textbox, devices, Blu):
    
    async_loop = asyncio.new_event_loop()
    #Gives the asyncio functions their own thread to run on (Allows for multiple functions to run at once)
    do_tasks(async_loop, WatchingData(devices, Blu))
    
    async_loop1 = asyncio.new_event_loop()
    
    do_tasks(async_loop1, DisplayData(textbox, devices))

async def WatchingData(devices, Blu):
    while Blu.collect_data:
        if  Blu.collection:
            devices.AddData(Blu.collection[0])
            Blu.collection.pop(0)

async def DisplayData(textbox, devices):
    while 1:
        if devices.collection:
            textbox.text_box.insert('end', devices.collection[0]+"\n")
            devices.collection.pop(0)
    

#Dad calls the KIDs that he needs to speak to
def send_message(devices):
    #Creates a new GUI
    messageBox = Tk()
    messageBox.title("Send Message")
    messageBox.geometry("350x350")
    
    #Keeps track of the KIDs the Dad is speaking to
    var = dict()
    
    for  i in range(len(devices.devices)):
        var[i] = Potential_devices(i,False)
        
        #If the checkmark is is given when submitted than the data is talking to this Child
        Checkbutton(messageBox, text=devices.devices[i], command=lambda key=var[i] : isChecked(key)).grid(row=i, sticky=W)
    
    #User input for the message sent
    inputtxt = Text(messageBox,height = 1,width = 40)
    inputtxt.grid(row = 40)
    
    #Dad sends the message to the speciefied children
    Button(messageBox,text = "Send", command = lambda: SND_MSS(messageBox,var, devices, inputtxt)).grid(row = 50)
    
    #Dad goes quite and doesn't speak to his children
    Button(messageBox,text = "Close", command = messageBox.destroy).grid(row = 60)
    
    messageBox.mainloop()

#Dad finally gives the select KIDs his talking to
def SND_MSS(root,val,devices, inputtxt):
    #Grab the user message and convert it to a string
    tmp = str(inputtxt.get(1.0, "end-1c"))
    
    #Checks all connected devices
    for i in range(len(devices.devices)):
        #Checks to see which KIDs were selected
        if (val[i].state):
            #Message is sent
            devices.BLU_dev[i].sendMessage(tmp)
            
def GrabFilePath(FileName, devices):
    #Creates a new GUI
    root = tk.Tk()
    root.title('Grab File Path')
    root.configure(background = 'light gray')
    root.geometry("450x50")
    root.update()
    
    #Button to select a file location to place the recorded data
    open_file = tk.Button(root, text = "Storage location",  command=lambda: [file_browser(FileName, root, devices)])
    open_file.place(x=150, y=10)

    root.mainloop()

#Save the file location for later use
def file_browser(FileName, master, devices):
    #Get the directory on where the file is going to be stored
    FileName.save_directory(fd.askdirectory())
    
    #Creates a new GUI
    root = tk.Tk()
    root.title('CSV Name')
    root.configure(background = 'light gray')
    root.geometry("350x100")
    
    #User input for the name of the new CSV file
    inputtxt = Text(root,height = 3,width = 40)
    inputtxt.grid(row = 40)
    
    #If clicked will create the file in the specified location
    Button(root,text = "Create", command = lambda: [CreateFile(FileName,inputtxt, devices), root.destroy(), master.destroy()]).grid(row = 50)
    root.mainloop()

#Creates the file in the specified location
def CreateFile(FileName, inputtxt, devices):
    #Update the file name
    FileName.update_name(str(inputtxt.get(1.0, "end-1c")))
    
    #Add the CSV extention
    FileName.name = FileName.name + ".csv"
    
    #Saves the entire path including file name (can be used to open csv)
    FileName.save_file()
    
    devices.File.Recording = True
    RecordingData(devices)
    
def RecordingData(devices):
   async_loop = asyncio.new_event_loop()
   do_tasks(async_loop, devices.CollectData())
    
def Discovery(root, Devices, Buttons, Display):
    async_loop = asyncio.new_event_loop()
    do_tasks(async_loop, Discover_Devices(root, Devices, Buttons, Display))
        
#Discoveres Devices to be selected to connect to 
async def Discover_Devices(root, conn_devices, buttons, display):
    #Discovers the available devices
    devices = bluetooth.discover_devices( lookup_names=True, lookup_class=True)
    
    #Turns the list into a set (sets don't allow duplication)
    devices_found = set(devices)
    
    #Find the difference between the already connected devices and the already connceted devices
    new_devices = devices_found.difference(set(conn_devices.devices))
    
    #Creates new GUI
    checkbox = Tk()
    checkbox.title('Add Device(s)')
    checkbox.geometry("450x350")
    
    #Will keep track of the KIDS had by the DAD
    var = dict()
    
    for  i in range(len(new_devices)):
        var[i] = Potential_devices(i,False)
        #Changes the state if wanted by the DAD
        Checkbutton(checkbox, text=devices[i], command=lambda key=var[i] : isChecked(key)).grid(row=i, sticky=W)
    
    #Turns the set to a list
    lis = list(new_devices)
    
    #Add the selected KIDs to the DAD
    Button(master = checkbox, text = 'Submit', command = lambda: check_states(checkbox,root, var, conn_devices, lis, buttons, display)).grid(row = 50)
        
    checkbox.mainloop()

def isChecked(key):
    #if selected or unselected will change state (False->True or True-False)
    key.change_state()

#Add the KIDS to the main GUI
def check_states(root,master, var_list, current, new, buttons, display):
    for i in range(len(var_list)):
        #If KID is selected
        if (var_list[i].state):
            
            #Append the name ot the connected KID
            current.new_device(new[i])
            
            #Finally makes the connection
            Added_Device(master,current,new[i][0], 'EKGKID_0', str(current.num) , 1,current.xpos, current.ypos, buttons, display, current)
            
            #Updates x position of KID buttons in the DAD
            current.update_xpos()
    
    root.destroy()
    
def do_tasks(async_loop, func):
    #Creates a new thread process and gives it a asyncio function to run to completion
    threading.Thread(target=_asyncio_thread, args=(async_loop,func)).start()

#Creates Buttons for added devices
def Added_Device(root,current, temp, device_type, num, port, xpos, ypos, buttons, display, overall_devices):
    #Creates functions that run in parallel to each other
    async_loop = asyncio.new_event_loop()
    #async_loop1 = asyncio.new_event_loop()
    #async_loop2 = asyncio.new_event_loop()
    
    #creates a BlueTooth device type 
    device = current.new_BLU(Bluetooth_Devices(device_type, num, temp, port))
    
    #Makes the Bluetooth connection
    device.MakeConnection()
    
    #Gives the asyncio functions their own thread to run on (Allows for multiple functions to run at once)
    do_tasks(async_loop, device.CollectData())
    #do_tasks(async_loop2, device.PlotData())
    #Button to be created 
    B1 = Button(master=root, text=device_type+num, command= lambda: device.ChangeCollecting())
    B2 = Button(master=root, text=device_type+num+"Plot", command= lambda: {device.ToggleGraph(), Main_recording_State(device)})
    B3 = Button(master=root, text=device_type+num+"Close", command= lambda: Graphing_Close(device))
    
    #Adds buttons to a list to keep track of
    buttons.add_Button([B1, B2, B3])
    
    #Places the Buttons in a specified order
    buttons.latest_Button()[0].place(x =xpos, y= ypos)
    buttons.latest_Button()[1].place(x =xpos, y= ypos+30)
    buttons.latest_Button()[2].place(x =xpos, y= ypos+60)
    Main_DisplayData(root, display, overall_devices, device)
    
def Main_recording_State(device):
    async_loop = asyncio.new_event_loop()
    do_tasks(async_loop, device.MakeGraph())

def DeviceRemoval(root, Devices, Buttons):
    async_loop = asyncio.new_event_loop()
    do_tasks(async_loop, Remove_Devices(root, Devices, Buttons))
    
def Graphing_Close(Blu):
    async_loop = asyncio.new_event_loop()
    do_tasks(async_loop, Blu.Close_graph())

#Selection for removal of a KID
async def Remove_Devices(root, devices, buttons):
    #Creates a new GUI
    checkbox = Tk()
    checkbox.title('Remove Device(s)')
    checkbox.geometry("450x350")
     
    #Keeps track of which KIDs are being removed 
    var = dict()
        
    for  i in range(len(devices.devices)):
        var[i] = Potential_devices(i,False)
        Checkbutton(checkbox, text=devices.devices[i], command=lambda key=var[i] : isChecked(key)).grid(row=i, sticky=W)
    
    #Removes the specified Devices
    Button(master = checkbox, text = 'Submit', command = lambda: Removal(checkbox, var, devices, buttons)).grid(row = 50)
     
    checkbox.mainloop()
    
#Removing the specified KIDs
def Removal(root, val, devices, buttons):
    #Runs the list backwards
    for i in range(len(devices.devices)-1,-1,-1):
        if (val[i].state):
            
            #Removes the specified KID
            devices.remove_device(i)
            
            #Removes its associated buttons
            buttons.remove_button(i)
            
    #Reorders the button order if removal has occured     
    Reorder_Buttons(devices, buttons)
    root.destroy()

def Reorder_Buttons(devices, buttons):
    #Default xpos and ypos
    devices.xpos = 0
    devices.ypos = 450
    
    #Reorders the buttons
    for button in buttons.Buttons:
         button[0].place(x = devices.xpos, y = devices.ypos)
         button[1].place(x = devices.xpos, y = devices.ypos+30)
         button[2].place(x = devices.xpos, y = devices.ypos+60)
         devices.update_xpos()