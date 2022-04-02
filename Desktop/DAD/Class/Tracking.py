class Current_devices:
    def __init__(self, devices = list(),BLU_dev = list(), num =-1, xpos = 0,ypos = 450):
        self.devices = devices
        self.BLU_dev = BLU_dev
        self.num = num
        self.xpos = xpos
        self.ypos = ypos
        
    def update_ypos(self,update_pos = 100):
        self.ypos = self.ypos + update_pos
    
    def update_xpos(self,update_pos = 125):
        self.xpos = self.xpos + update_pos
        if(self.xpos > 500):
            self.xpos = 0
            self.update_ypos()
    
    def new_device(self, device):
        self.devices.append(device)
        self.num = self.num + 1
    
    def new_BLU(self, BLU):
        self.BLU_dev.append(BLU)
        return BLU
        
    def latest_BLU(self):
        return self.BLU_dev[self.num] 
        
    def remove_device(self, pos):
        self.devices.pop(pos)
        self.BLU_dev[pos].CloseConnection()
        self.BLU_dev.pop(pos)
        self.num = self.num - 1
        
class Potential_devices:
    def __init__(self, device_num, state):
        self.device_num = device_num
        self.state = False
    
    def change_state(self):
        self.state = not self.state
        
class Current_Buttons:
    def __init__(self, Buttons = list()):
        self.Buttons = Buttons
        self.counter = -1
        
    def add_Button(self, Button):
        self.counter = self.counter + 1
        self.Buttons.append(Button)
    
    def latest_Button(self):
        return self.Buttons[self.counter]
    
    def remove_button(self, pos):
        self.Buttons[pos][0].destroy()
        self.Buttons[pos][1].destroy()
        self.Buttons[pos][2].destroy()
        self.Buttons.pop(pos)
        self.counter = self.counter - 1
