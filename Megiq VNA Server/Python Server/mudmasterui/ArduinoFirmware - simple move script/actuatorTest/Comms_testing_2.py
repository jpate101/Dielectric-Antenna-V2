# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 10:11:04 2024

@author: JoshuaPaterson
"""

import serial

# Connect to Arduino
arduino = serial.Serial('COM3', 9600)  # Replace 'COM3' with your Arduino's serial port

# Send command to move actuator out
command = 'A\n'
arduino.write(command.encode())

# Close the serial connection
arduino.close()