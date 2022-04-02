import bluetooth
import struct
import asyncio
from tkinter import *
from Graphing import *

class Bluetooth_Devices:
    def __init__(self, DataType, DeviceNumber, Address, port):
        self.DataType = DataType
        self.DeviceNumber = DeviceNumber
        self.Address = Address
        self.port = port
        self.data = ""
        self.state = False
        self.solo_plot_state = False
        self.collection = list()
     
    def MakeConnection(self):
        self.s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.s.connect((self.Address, self.port))
        print("Connection Made")
    
    def CloseConnection(self):
        self.s.close()
        
    def ChangeCollecting(self,closing = False):
        if closing:
            ba = struct.pack("?",False)
            self.s.send(ba)
        else:
            self.state = not(self.state)
            ba = struct.pack("?",self.state)
            self.s.send(ba)
    
    def ToggleGraph(self):
        print("Hello")
    
    def SoloGraph(self):
        self.self.solo_plot_state = not(self.self.solo_plot_state)
        
    async def PlotData(self):
        while 1:
            root = Tk()
            root.title(self.DataType+ self.DeviceNumber+' Graph')
            root.configure(background = 'light gray')
            #root.geometry("605x450")
            root.geometry("300x300")
            
            make_plot = Plotting_EMG(root,300,300)
            #while self.solo_plot_state:
            #   
            root.mainloop()
                
        
    def sendMessage(self, message):
        b = b''
        message = b + message.encode('utf-8')
        self.s.send(message)
    
    async def CollectData(self):
        count = 0
        while 1:
            while self.state:
                self.data = ""
                while count < 2:
                    d = self.s.recv(4096)
                    self.data += (str(d.decode("utf-8")))
                    count += 1
                if(self.data != ""):
                    self.collection.append(self.data)
                count = 0
                print("Received: " + self.data + " from Device: " +self.DeviceNumber)
            #await asyncio.sleep(0.1)