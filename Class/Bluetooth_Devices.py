from bleak import BleakScanner,BleakClient
import struct
import asyncio
import time
import threading
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from tkinter import *
import numpy as np
#from Functions import * Do not uncomment otherwise Bluetooth will not connect to any device

class Bluetooth_Devices:
    def __init__(self, Address, name):
        
        self.UUID = "b568e651-7afb-4bcd-809b-9b7769361e28"
          
        self.name = name
        
        #Address of the bluetooth device
        self.Address = Address
        
        self.client = BleakClient(self.Address)
        
        #storage for incoming data
        self.data = ""
        
        #Allows the DAD to toggle the KIDS talking
        self.state = False
        
        #Will be used to toggle a solo plot for each KID
        self.solo_plot_state = False
        
        #Will be used for the solo plot
        self.collection = list()
        
        self.collect_data = True
        
        self.Collect_data_while = True
        
        self.PlotData_main = True
        
        self.recordingCollection = list()
        
        self.plot = plt
        
        self.z = np.empty( shape=(0, 0) )
        
    def init(self):
            self.line.set_data([1, 2],[0,0])
            return self.line,
     
    def MakeConnection(self):
        #Create the Socket for the connection
        print("")
    
    async def CloseConnection(self):
        #Closing the connection
        self.client.disconnect()
        print("Please Close")
        
    def ChangeCollecting(self, Closing = False):
        if Closing:
           # ba = struct.pack("?",False)
            self.CloseConnection
        else:
            self.state = not(self.state)
            #ba = struct.pack("?",self.state)
            #self.s.send(ba)
    
    def ToggleGraph(self):
        self.solo_plot_state = not(self.solo_plot_state)
        
    async def MakeGraph(self):
        
        def SoloGraph(i):
            win = 50
            time.sleep(0.15)
            while self.solo_plot_state:
                imin = min(max(0, i-win), i)
                x = np.arange(len(self.recordingCollection)) + 1
                if x.size != self.z.size:
                    y = np.asarray(self.recordingCollection) 
                    xdata = x[imin:i]
                    ydata = y[imin:i]
                    self.line.set_data(xdata, ydata)
                    self.ax.relim()
                    self.ax.autoscale()
                    self.z = x
                    return self.line,
        self.fig, self.ax = self.plot.subplots()
        self.line, = self.ax.plot([], [], 'k-')
        self.ax.margins(0.05)
        
        anim = animation.FuncAnimation(self.fig, SoloGraph, init_func=self.init)
        threading.Thread(target=anim).start()
            
        self.plot.show()
                
    async def Close_graph(self):
        self.solo_plot_state = False
        #self.fig.delaxes(self.ax)
        self.plot.close()
                      
    def sendMessage(self, message):
        #Makes sure that the message is a byter
        b = b''
        
        #encrpyting the message 
        message = b + message.encode('utf-8')
        
        client.write_gatt_char(data = message,char_specifier  = self.UUID, response =False)
        
    def callback(self,sender: int, data: bytearray):
        int_data = [x for x in data]
        #print(f"{sender}: {int_data[6]}")
        #Add data to a collection that will be used to display data
        if(self.collect_data):
            temp = "Received: " + str(int_data[6]) + " from Device: " +self.name
            self.collection.append([temp,[self.name,int_data[6]]])
        if(self.solo_plot_state):
            self.recordingCollection.append(int_data[6])

    
    async def CollectData(self):
        await self.client.connect()
        print("Connection Made")
        while self.Collect_data_while:
            #Will only run if the DAD wants to talk to its KID (default = False)
            await self.client.start_notify(self.UUID, self.callback) 
            while self.state:
                await self.client.write_gatt_char(data = b"\x50\x01\x08",char_specifier  = self.UUID, response =True)
            #await asyncio.sleep(0.1)
                
    def TURN_OFF(self):
        self.state = False
        self.ChangeCollecting(Closing = True)
        self.solo_plot_state = False
        self.collect_data = False
        self.Collect_data_while = False
        #self.Close_graph()
        self.CloseConnection()