from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
import asyncio

class Plotting_EMG:
    def __init__(self, root, width_, height_):
        self.root = root
        self.fig = Figure()
        ax = self.fig.add_subplot(111)

        ax.set_title('plotter')
        ax.set_xlabel('Sample')
        ax.set_ylabel('Voltage')
        ax.set_xlim(0,100)
        ax.set_ylim(0.10,3.5)
        lines = ax.plot([],[])[0]

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().place(x=10,y=10,width=width_,height=height_)
        self.canvas.draw()
        
        async def CollectData(self):
            print("hello")


#open_file = tk.Button(root, text = "Bluetooth ON", font = ('calibri', 12), command=lambda: [bluetooth_toggle(),data_received()])
#open_file.place(x=stop.winfo_x()+start.winfo_reqwidth() + 20, y=450)

#root.update()
#open_file = tk.Button(root, text = "Open File", font = ('calibri', 12), command=lambda: file_brows())
#open_file.place(x=stop.winfo_x()+start.winfo_reqwidth() + 160, y=450)

#root.after(1,plot_data_2)
#root.mainloop()
