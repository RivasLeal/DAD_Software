import bluetooth
import struct
import asyncio
from tkinter import *
from Graphing import *

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
        
        self.RecordState = False
        
        #Will be used for the solo plot
        self.collection = list()
        
        self.collect_data = True
        
        self.Collect_data_while = True
        
        self.PlotData_while = True
     
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
        print("Hello")
    
    def SoloGraph(self):
        #Toggling the state
        self.self.solo_plot_state = not(self.self.solo_plot_state)
        
    async def PlotData(self):
        while self.PlotData_while:
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
        self.PlotData_while = False
        self.CloseConnection()