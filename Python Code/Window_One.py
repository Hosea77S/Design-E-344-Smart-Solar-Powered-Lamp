# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 17:35:15 2021

@author: Siphiwe
"""


#from IPython import get_ipython;   
#get_ipython().magic('reset -sf')

import tkinter as tk
import tkinter.ttk as tkt
from tkinter import font as tkfont  # python 3

from tkinter import messagebox
import SerialComms

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as fcta
import time

class Window_One():
    
    baudLableText = "Enter the Baud Rate"
    comLableText = "Enter the Comm Port"
    graphWindow_name = "GraphWindow"
    
    SupplyVoltageLableText = "Supply Voltage [V]"
    VS = 0.0
    BatteryVoltageLableText = "Battery Voltage [V]"
    VB = 0.0
    BatteryCurrentLableText = "Battery Current [mA]"
    IB = 0.0
    LightLevelLableText = "Ambient Light [%]"
    AmbL = 0.0
    pwlLableText = "Choose a Load brightness [%]"
    vb_data = np.array([])
    vs_data = np.array([])
    ib_data = np.array([])
    ambl_data = np.array([])
    
    width = 800
    height = 600
    xpos = 300
    ypos = 150
    def __init__(self, sc, WindowTitle):
        self.sc = sc
        self.window = tk.Tk()
        self.label_font = tkfont.Font(family='Helvetica', size=15, weight="bold", slant="italic")
        self.output_font = tkfont.Font(family='Helvetica', size=15, weight="bold", slant="italic")
        self.style = tkt.Style()
        self.output_style = tkt.Style()
        self.setTheme()
        self.window.title(WindowTitle)
        self.window.geometry('%dx%d+%d+%d' %(self.width, self.height, self.xpos, self.ypos) )
        self.window.resizable(False, False)
        
        self.createTabs()
        self.create_labels()
        self.create_entries()
        self.create_buttons()
        self.create_VBplot(10, 5, 370, 250)
        self.create_VSplot(15+370, 5, 370, 250)
        self.create_IBplot(10, 10+250, 370, 250)
        self.create_AmbLplot(15+370, 10+250, 370, 250)
        self.window.update();
        #self.createSlider()
        
    def setTheme(self):
        self.style = tkt.Style()
        self.style.theme_use('alt')
        
    def createTabs(self):
        self.tabControl = tkt.Notebook(self.window)
        self.tab1 = tkt.Frame(self.tabControl)
        self.tab2 = tkt.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text='Main Tab')
        self.tabControl.add(self.tab2, text='Graphic Window')
        self.tabControl.pack(expand=1, fill="both")
        
    def create_buttons(self):
        ##
        self.graphButton = tkt.Button(self.tab1, text="Toggle Connection", style="big.TButton") #, font=self.button_font)# command=lambda: self.open_graph())
        self.graphButton.grid(column=1, row=3, padx=2, pady=2)
        
        self.chargeOnButton = tkt.Button(self.tab1, text="Switch ON Charging", style="big.TButton")# command=lambda: self.open_graph())
        self.chargeOnButton.grid(column=1, row=10, padx=2, pady=2)
        
        self.chargeOffButton = tkt.Button(self.tab1, text="Switch OFF Charging", style="big.TButton")# command=lambda: self.open_graph())
        self.chargeOffButton.grid(column=2, row=10, padx=2, pady=2)
        
        self.pwlButton = tkt.Button(self.tab1, text="Set Load Brightness", style="big.TButton")# command=lambda: self.open_graph())
        self.pwlButton.grid(column=2, row=9, padx=2, pady=2)
        
        self.style.configure('big.TButton', font=(None, 15), foreground="blue4")
        
    def create_labels(self):
        ##
        ##Baud Rate label
        self.baudlabel = tkt.Label(self.tab1, text=self.baudLableText, font=self.label_font)
        self.baudlabel.grid(column=0, row=1, padx=2, pady=2)
        
        ##Com Port Label
        self.comlabel = tkt.Label(self.tab1, text=self.comLableText, font=self.label_font)
        self.comlabel.grid(column=0, row=2, padx=2, pady=2)
        
        self.chargelabel = tkt.Label(self.tab1, text="not connected", font=self.label_font)
        self.chargelabel.grid(column=2, row=3, padx=2, pady=2)
        
        ##Supply Voltage label
        self.SupplyVoltageLable = tkt.Label(self.tab1, text=self.SupplyVoltageLableText, font=self.label_font)
        self.SupplyVoltageLable.grid(column=0, row=6, padx=2, pady=2)
        self.VSLable = tkt.Label(self.tab1, text= str(self.VS) , font=self.label_font, style="BW.TLabel")
        self.VSLable.grid(column=1, row=6, padx=2, pady=2)
        
        ##Battery Voltage label
        self.BatteryVoltageLable = tkt.Label(self.tab1, text=self.BatteryVoltageLableText, font=self.label_font)
        self.BatteryVoltageLable.grid(column=0, row=5, padx=2, pady=2)
        self.VBLable = tkt.Label(self.tab1, text=str(self.VB), font=self.label_font, style="BW.TLabel")
        self.VBLable.grid(column=1, row=5, padx=2, pady=2)
    
        ##Battery Current label
        self.BatteryCurrentLable = tkt.Label(self.tab1, text=self.BatteryCurrentLableText, font=self.label_font)
        self.BatteryCurrentLable.grid(column=0, row=7, padx=2, pady=2)
        self.IBLable = tkt.Label(self.tab1, text=str(self.IB), font=self.label_font, style="BW.TLabel")
        self.IBLable.grid(column=1, row=7, padx=2, pady=2)
        
        ##Light level label
        self.LightLevelLable = tkt.Label(self.tab1, text=self.LightLevelLableText, font=self.label_font)
        self.LightLevelLable.grid(column=0, row=8, padx=2, pady=2)
        self.AmbLable = tkt.Label(self.tab1, text=str(self.AmbL), font=self.label_font, style="BW.TLabel")
        self.AmbLable.grid(column=1, row=8, padx=2, pady=2)
        
        self.pwlLable = tkt.Label(self.tab1, text=self.pwlLableText, font=self.label_font)
        self.pwlLable.grid(column=0, row=9, padx=2, pady=2)
        
        self.output_style.configure("BW.TLabel", foreground= "white", background="blue")

    def create_entries(self):
        ##
        ##Baud Rate Entry
        self.entryBaudRate = tkt.Entry(self.tab1, font=self.label_font)
        self.entryBaudRate.grid(column = 1, row = 1, padx=2, pady=2)
        self.entryBaudRate.insert(0,"9600")
        
        ##Com Port Entry
        self.entryComPort = tkt.Entry(self.tab1, font=self.label_font)
        self.entryComPort.grid(column = 1, row = 2, padx=2, pady=2)
        self.entryComPort.insert(0,"COM11")
        
        self.entrypwl = tkt.Entry(self.tab1, font=self.label_font)
        self.entrypwl.grid(column = 1, row = 9, padx=2, pady=2)
        self.entrypwl.insert(0,"50")
        
    #def open_graph(self):
        #self.graphWindow.open_page(True)
        
    def createSlider(self):
        self.slider = tkt.Scale(self.tab1, from_=0, to=100)
        self.slider.grid(column=0, row=9)
        
    def create_VBplot(self, px, py, pwidth, pheight):
        self.vb_fig = Figure();
        self.ax = self.vb_fig.add_subplot(111)
        
        self.ax.set_title('Battery Voltage (V)')
        self.ax.set_xlabel('time (seconds)')
        #self.ax.set_ylabel('Voltage (V)')
        self.ax.set_xlim(0,60)
        self.ax.set_ylim(5.9, 7.3)
        self.vb_lines = self.ax.plot([],[])[0]
        
        self.vb_canvas = fcta(self.vb_fig, master=self.tab2)
        self.vb_canvas.get_tk_widget().place(x = px, y = py, width=pwidth, height=pheight)
        self.vb_canvas.draw()
        
    def create_VSplot(self, px, py, pwidth, pheight):
        self.vs_fig = Figure();
        self.bx = self.vs_fig.add_subplot(111)
        
        self.bx.set_title('Supply Voltage (V)')
        self.bx.set_xlabel('time (seconds)')
        #self.bx.set_ylabel('Voltage (V)')
        self.bx.set_xlim(0,60)
        self.bx.set_ylim(0, 24)
        self.vs_lines = self.bx.plot([],[])[0]
        
        self.vs_canvas = fcta(self.vs_fig, master=self.tab2)
        self.vs_canvas.get_tk_widget().place(x = px, y = py, width=pwidth, height=pheight)
        self.vs_canvas.draw()
        
    def create_IBplot(self, px, py, pwidth, pheight):
        self.ib_fig = Figure();
        self.cx = self.ib_fig.add_subplot(111)
        
        self.cx.set_title('Battery Current (mA)')
        self.cx.set_xlabel('time (seconds)')
        #self.cx.set_ylabel('current (mA)')
        self.cx.set_xlim(0,60)
        self.cx.set_ylim(-150, 400)
        self.ib_lines = self.cx.plot([],[])[0]
        
        self.ib_canvas = fcta(self.ib_fig, master=self.tab2)
        self.ib_canvas.get_tk_widget().place(x = px, y = py, width=pwidth, height=pheight)
        self.ib_canvas.draw()
    
    def create_AmbLplot(self, px, py, pwidth, pheight):
        self.ambl_fig = Figure();
        self.dx = self.ambl_fig.add_subplot(111)
        
        self.dx.set_title('Ambient Light (%)')
        self.dx.set_xlabel('time (seconds)')
        #self.dx.set_ylabel('Voltage (V)')
        self.dx.set_xlim(0,60)
        self.dx.set_ylim(0, 100)
        self.ambl_lines = self.dx.plot([],[])[0]
        
        self.ambl_canvas = fcta(self.ambl_fig, master=self.tab2)
        self.ambl_canvas.get_tk_widget().place(x = px, y = py, width=pwidth, height=pheight)
        self.ambl_canvas.draw()
    
    def plot_data(self):
        ##Battery Voltage Plot
        if (len(self.vb_data) < 60):
            self.vb_data = np.append(self.vb_data, self.VB)
        else:
            self.vb_data[0:59] = self.vb_data[1:60]#shift left
            self.vb_data[59] = self.VB#add next data point
            #print(str(self.vb_data[59]))
        self.vb_lines.set_xdata(np.arange(0, len(self.vb_data)))
        self.vb_lines.set_ydata(self.vb_data)
        self.vb_canvas.draw()
        
        ##Supply Voltage plot
        if (len(self.vs_data) < 60):
            self.vs_data = np.append(self.vs_data, self.VS)
        else:
            self.vs_data[0:59] = self.vs_data[1:60]#shift left
            self.vs_data[59] = self.VS#add next data point
            #print(str(self.vs_data[59]))
        self.vs_lines.set_xdata(np.arange(0, len(self.vs_data)))
        self.vs_lines.set_ydata(self.vs_data)
        self.vs_canvas.draw()
        
        ##Battery Current Plot
        if (len(self.ib_data) < 60):
            self.ib_data = np.append(self.ib_data, self.IB)
        else:
            self.ib_data[0:59] = self.ib_data[1:60]#shift left
            self.ib_data[59] = self.IB#add next data point
            #print(str(self.ib_data[59]))
        self.ib_lines.set_xdata(np.arange(0, len(self.ib_data)))
        self.ib_lines.set_ydata(self.ib_data)
        self.ib_canvas.draw()
        
        ##Ambient light plot
        if (len(self.ambl_data) < 60):
            self.ambl_data = np.append(self.ambl_data, self.AmbL)
        else:
            self.ambl_data[0:59] = self.ambl_data[1:60]#shift left
            self.ambl_data[59] = self.AmbL#add next data point
            #print(str(self.ambl_data[59]))
        self.ambl_lines.set_xdata(np.arange(0, len(self.ambl_data)))
        self.ambl_lines.set_ydata(self.ambl_data)
        self.ambl_canvas.draw()
       
    
    def open_page(self):
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()
        
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            print("closing main")
            if(self.sc.isOpen == True):
                self.sc.close()
            #self.graphWindow.close_window()
            self.window.destroy()
        
#page = Window_One()
#page.open_page()