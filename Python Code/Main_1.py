# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 17:34:31 2021

@author: Siphiwe
"""

#import Integrator

#mainInt = Integrator.Integrator(1, 3, 200000)
from IPython import get_ipython;   
get_ipython().magic('reset -sf')

import Window_One as w
import SerialComms
from serial import SerialException

comPort = "COM11"
baudRate = "9600"

sc = SerialComms.SerialComms(comPort, baudRate)
mainpage = w.Window_One(sc, "E.Design Application")
mainpage.graphButton.configure(command = lambda: buttonConnectHandler())
mainpage.chargeOnButton.configure(command = lambda: buttonChargeHandler(1))
mainpage.chargeOffButton.configure(command = lambda: buttonChargeHandler(0))
mainpage.pwlButton.configure(command = lambda: setpwl())

def open_connection():
    print("yes")
    
# updates the display every 100 ms
def updateDisplay():
    # update the variables that you want to stay current here
    if(sc.isOpen==True):
        data = sc.receive()
    
        if(len(data) > 1):
            print(data[0])
            updateWindowData(data[0])
            mainpage.plot_data()
            
        data = ""

    mainpage.window.after(1000,lambda: updateDisplay())

def openConnection(sc):
    sc.setCOMPort(comPort)
    sc.setBaudrate(baudRate)
    sc.open()
    
def closeConnection(sc):
    sc.close()
    
def buttonConnectHandler():
    global comPort
    global baudRate

    #If the connection is closed, try open it.
    if(sc.isOpen == False):
        comPort = mainpage.entryComPort.get()
        baudRate = mainpage.entryBaudRate.get()
        
        #Tries to open the serial conection. Displays error message in ConnectFeedback if it fails.
        try:
            openConnection(sc);
        except SerialException:
            print("Unable to connect.")
            mainpage.chargelabel.config(text="Unable to connect.")
        if(sc.isOpen == True):
            print("Connected successfully.")
            mainpage.chargelabel.config(text="connected")
    
    #If the connection is open, close it.        
    elif(sc.isOpen==1):
        #Tries to close the serial conection. Displays error message in ConnectFeedback if it fails.
        try:
            closeConnection(sc)
        except SerialException:
            print("Unable to close connection.")
            mainpage.chargelabel.config(text="Unable to close connection.")
        #If the connection is closed, change the label of the button and and update ConnectFeedback to disconnected.
        if(sc.isOpen == False):
            print("Disconnected successfully.")
            mainpage.chargelabel.config(text="disconnected")
            #connectionStatusLabel.configure(text = "The device is currently disconnected.")
            
def buttonChargeHandler(ov_state):
    if(sc.isOpen == True):
        if(ov_state == 1):
            sc.send("OV1")    
        if(ov_state == 0):
            sc.send("OV0")  
            
def updateWindowData(serial_data):
    data_array = serial_data.split(sep=",", maxsplit=5)
    mainpage.VBLable.configure(text=data_array[1])
    mainpage.VB = float(data_array[1])
    mainpage.VSLable.configure(text=data_array[2])
    mainpage.VS = float(data_array[2])
    mainpage.IBLable.configure(text=data_array[3])
    mainpage.IB = float(data_array[3])
    mainpage.AmbLable.configure(text=data_array[4])
    mainpage.AmbL = float(data_array[4])
    
def setpwl():
    dutycycle = int(mainpage.entrypwl.get())
    
    if (dutycycle > 100):
        dutycycle = 100
        mainpage.entrypwl.configure(text=str(dutycycle))
    elif (dutycycle < 0):
        dutycycle = 0
        mainpage.entrypwl.configure(text=str(dutycycle))
    
    if(sc.isOpen == True):
        message = ""
        message = "P" + str(dutycycle)
        sc.send(message)
    
updateDisplay()
mainpage.open_page()