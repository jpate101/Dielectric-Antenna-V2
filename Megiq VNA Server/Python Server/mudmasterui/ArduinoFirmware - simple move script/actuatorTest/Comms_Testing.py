# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 12:55:28 2024

@author: JoshuaPaterson
"""

import os
import requests
import time
import threading
import json
import serial
import serial.tools.list_ports

deviceDescriptions = ['Arduino']
_serialPort = None

            

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


    
    
    
if __name__ == '__main__':
    
    availablePorts = findSerialPorts()
    if(len(availablePorts) >= 1):
        # found the arduino
        print('Found Arduino')
        print(availablePorts)
        _serialPort = serial.Serial(port = availablePorts[0].device, 
                                        baudrate = 9600, 
                                        timeout = 1.0, 
                                        bytesize = serial.EIGHTBITS)

        _serialNo = availablePorts[0].serial_number

        print('Serial No.:', _serialNo)
        print('connected')
        
        command = '{}'.format('A\n')
        #command = command + '\n\r'
        try:
            print("in try")
            _serialPort.write(command.encode())

        except Exception as e:
            print('Communication Error: permission. {}'.format(e))


    pass