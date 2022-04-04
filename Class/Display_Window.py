from tkinter import *

class DisplayWindow:
    def __init__(self, root):
        self.root = root
        #self.frame = Frame(self.root)
        self.text_box = Text(self.root,width=30,height = 45,wrap='word')
        #text_box.insert('end', message)
        self.text_box.config(state='normal')
        self.text_box.see("end")
        self.text_box.place(x = 550 , y = 0)

        sb = Scrollbar(self.root)
        sb.pack(side=RIGHT, fill=BOTH)

        self.text_box.config(yscrollcommand=sb.set)
        sb.config(command=self.text_box.yview)
    