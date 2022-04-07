import bluetooth
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
    def __init__(self, DataType, DeviceNumber, Address, port):
        #Data Type of the device
        self.DataType = DataType
        
        #Device Number (may become absolete and combined with datatype to become Name)
        self.DeviceNumber = DeviceNumber
        
        #Address of the bluetooth device
        self.Address = Address
        
        #Port for establishing a connection
        self.port = port
        
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
        self.s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        
        #Establishing the Connection
        self.s.connect((self.Address, self.port))
        print("Connection Made")
    
    def CloseConnection(self):
        #Closing the connection
        self.s.close()
        
    def ChangeCollecting(self, Closing = False):
        if Closing:
            ba = struct.pack("?",False)
            self.s.send(ba)
        else:
            self.state = not(self.state)
            ba = struct.pack("?",self.state)
            self.s.send(ba)
    
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
        
        #Sending the message
        self.s.send(message)
    
    async def CollectData(self):
        #Used to make sure the Gui has time to collect the data
        count = 0
        
        while self.Collect_data_while:
            #Will only run if the DAD wants to talk to its KID (default = False)
            while self.state:
                
                #Clears The current data
                data = ""
                
                while count < 2:
                    #Recieves data from buffer
                    d = self.s.recv(4096)
                    
                    #Adds the data to itself
                    data += (str(d.decode("utf-8")))
                    count += 1
                    
                #Add data to a collection that will be used to display data
                if(data != "" and self.collect_data):
                    temp = "Received: " + data + " from Device: " +self.DeviceNumber
                    self.collection.append([temp,data])
                if(self.solo_plot_state):
                    try:
                        self.recordingCollection.append(float(data))
                    except:
                        print("Data came in to fast")
                    
                #Resets Count
                count = 0
                
                #Prints data received
                print("Received: " + data + " from Device: " +self.DeviceNumber)
            #await asyncio.sleep(0.1)
                
    def TURN_OFF(self):
        self.state = False
        self.ChangeCollecting(Closing = True)
        self.solo_plot_state = False
        self.collect_data = False
        self.Collect_data_while = False
        #self.Close_graph()
        self.CloseConnection()