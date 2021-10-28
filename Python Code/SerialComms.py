##
## SerialComms.py
##
## SerialComms - A class for serial communication with an Arduino; for use in Design (E.) 344.
## Original Author: R.D. Beyers (last update 25/08/2015)
## Subsequent Edits: K.M. Coetzer
##
## This is free software - you may redistribute and modify it freely.
## This software is provided without any warranty.

import serial

class SerialComms():

    ## Class constructor - automatically called when instantiated
    ## Need to pass the COM port and baudrate as arguments
    ## Example: s = SerialComms('COM6', 19200)
    def __init__(self, COMPort, baudrate):
        self.COMPort = COMPort
        self.baudrate = baudrate
        self.isOpen = False

    ## Method for receiving serial data from the Arduino
    ## Empties the serial buffer into self.buf
    ## Separates messages on newline characters ('\n') and stores all the received messages in an array
    def receive(self):
        self.buf = ''
        messageArray = []
        numCharsRead = 0
        if (self.isOpen):
            while(self.serial.inWaiting() > 0):
                self.buf = self.buf + self.serial.read().decode("ascii")
                numCharsRead += 1
            if (numCharsRead > 0):
                self.buf = self.buf.rstrip('\n')
                messageArray = self.buf.split('\n')
        return messageArray

    ## Sends "message" to the Arduino
    ## Automatically adds a newline character ('\n') to tell the Arduino where the message ends
    def send(self, message):
        self.serial.write(str(message + "\n").encode())

    ## Closes the serial connection
    def close(self):
        self.isOpen = False
        self.serial.close()

    ## Opens the serial connection using the specified COM port and baud rate
    def open(self):
        self.serial = serial.Serial(self.COMPort, self.baudrate)
        self.isOpen = True

    ## Sets the COM port
    ## Has no effect on a currently active serial connection, until it is closed and re-opened
    def setCOMPort(self, COMPort):
        self.COMPort = COMPort

    ## Sets the baud rate
    ## Has no effect on a currently active serial connection, until it is closed and re-opened
    def setBaudrate(self, baudrate):
        self.baudrate = baudrate
