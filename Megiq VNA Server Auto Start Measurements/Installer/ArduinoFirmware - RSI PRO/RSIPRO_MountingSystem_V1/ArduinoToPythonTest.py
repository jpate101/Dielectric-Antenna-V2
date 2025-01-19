# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 12:07:45 2024

@author: JoshuaPaterson
"""

import serial
import time
import serial.tools.list_ports

deviceDescriptions = ['Arduino']

def findSerialPorts():
    """ @brief  Finds all serial devices connected to the system and makes a list of 
                the ports.
        @param  None
        @retval List of serial ports

    """
    portList = []
    comports = list(serial.tools.list_ports.comports())
    for p in comports:
        if any(desc in p.description for desc in deviceDescriptions):
            print(p, '<description:>', p.description, '<manufacturer:>', p.manufacturer, '<product:>', p.product, '<description length:>', len(p.description))
            portList.append(p)

    return portList

#arduino = serial.Serial(port='COM3',   baudrate=9600, timeout=.1)

availablePorts = findSerialPorts()
if(len(availablePorts) >= 1):
     # found the arduino
     print('Found Arduino')
     print(availablePorts)
     _serialPort = serial.Serial(port = availablePorts[0].device, 
                                     baudrate = 9600, 
                                     timeout = 1.0, 
                                     bytesize = serial.EIGHTBITS)

arduino = _serialPort



def write_read(x):
    arduino.write(bytes(x,   'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return   data


while True:
    num = input("Enter a number: ")
    value   = write_read(num)
    print(value)
