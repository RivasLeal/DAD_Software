import asyncio
import threading
import tkinter as tk
from tkinter import *
from Tracking import *
from Bluetooth_Devices import *

def _asyncio_thread(async_loop,func):
    async_loop.run_until_complete(func)
    
def send_message(devices):
    messageBox = Tk()
    messageBox.title("Send Message")
    messageBox.geometry("450x350")
    
    var = dict()
    
    for  i in range(len(devices.devices)):
        var[i] = Potential_devices(i,False)
        Checkbutton(messageBox, text=devices.devices[i], command=lambda key=var[i] : isChecked(key)).grid(row=i, sticky=W)
    
    inputtxt = Text(messageBox,height = 5,width = 20)
    inputtxt.grid(row = 40)
      
    Button(messageBox,text = "Print", command = lambda: SND_MSS(messageBox,var, devices, inputtxt)).grid(row = 50)
    
    messageBox.mainloop()

def SND_MSS(root,val,devices, inputtxt):
    tmp = str(inputtxt.get(1.0, "end-1c"))
    for i in range(len(devices.devices)):
        if (val[i].state):
            devices.BLU_dev[i].sendMessage(tmp)
            
    root.destroy()

def Discover_Devices(root, conn_devices, buttons):
    devices = bluetooth.discover_devices( lookup_names=True, lookup_class=True)
    devices_found = set(devices)
    new_devices = devices_found.difference(set(conn_devices.devices))
        
    checkbox = Tk()
    checkbox.title('Add Device(s)')
    checkbox.geometry("450x350")
        
    var = dict()
    
    for  i in range(len(new_devices)):
        var[i] = Potential_devices(i,False)
        Checkbutton(checkbox, text=devices[i], command=lambda key=var[i] : isChecked(key)).grid(row=i, sticky=W)
        
    lis = list(new_devices)    
    Button(master = checkbox, text = 'Submit', command = lambda: check_states(checkbox,root, var, conn_devices, lis, buttons)).grid(row = 50)
        
    checkbox.mainloop()

def isChecked(key):
    key.change_state()

def check_states(root,master, var_list, current, new, buttons):
    for i in range(len(var_list)):
        if (var_list[i].state):
            current.new_device(new[i])
            Added_Device(master,current,new[i][0], 'EKGKID_0', str(current.num) , 1,current.xpos, current.ypos, buttons)
            current.update_xpos()
    
    root.destroy()

def do_tasks(async_loop, func):
    """ Button-Event-Handler starting the asyncio part. """
    threading.Thread(target=_asyncio_thread, args=(async_loop,func)).start()
    
def Added_Device(root,current, temp, device_type, num, port, xpos, ypos, buttons):
    async_loop = asyncio.new_event_loop()
    #async_loop1 = asyncio.new_event_loop()
    async_loop2 = asyncio.new_event_loop()
    
    device = current.new_BLU(Bluetooth_Devices(device_type, num, temp, port))
    device.MakeConnection()
    
    do_tasks(async_loop, device.CollectData())
    #do_tasks(async_loop1, device.Data())
    #do_tasks(async_loop2, device.PlotData())
    
    B1 = Button(master=root, text=device_type+num, command= lambda: device.ChangeCollecting())
    B2 = Button(master=root, text="TogglePlot", command= lambda: device.ToggleGraph())
    B3 = Button(master=root, text="SoloGraph", command= lambda: device.SoloGraph())
    
    buttons.add_Button([B1, B2, B3])
    buttons.latest_Button()[0].place(x =xpos, y= ypos)
    buttons.latest_Button()[1].place(x =xpos, y= ypos+30)
    buttons.latest_Button()[2].place(x =xpos, y= ypos+60)
    
def Remove_Devices(root, devices, buttons):
    
     checkbox = Tk()
     checkbox.title('Remove Device(s)')
     checkbox.geometry("450x350")
     
     var = dict()
        
     for  i in range(len(devices.devices)):
         var[i] = Potential_devices(i,False)
         Checkbutton(checkbox, text=devices.devices[i], command=lambda key=var[i] : isChecked(key)).grid(row=i, sticky=W)
          
     Button(master = checkbox, text = 'Submit', command = lambda: Removal(checkbox, var, devices, buttons)).grid(row = 50)
     
     checkbox.mainloop()

def Removal(root, val, devices, buttons):
    for i in range(len(devices.devices)-1,-1,-1):
        if (val[i].state):
            devices.remove_device(i)
            buttons.remove_button(i)
            
    Reorder_Buttons(devices, buttons)
    root.destroy()

def Reorder_Buttons(devices, buttons):
    devices.xpos = 0
    devices.ypos = 450
    
    for button in buttons.Buttons:
         button[0].place(x = devices.xpos, y = devices.ypos)
         button[1].place(x = devices.xpos, y = devices.ypos+30)
         button[2].place(x = devices.xpos, y = devices.ypos+60)
         devices.update_xpos()