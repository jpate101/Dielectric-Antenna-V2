"""
*******************************************************************************
@file   interface_MountingSystem.py
@author Scott Thomason
@date   30 Sep 2021
@brief  Interface for the mounting system. This controls the actuator that 
        adjusts the height. It keeps track of the current system height and 
        adjusts it to ensure it is at the desired height.

REFERENCE:

*******************************************************************************
    Functions
*******************************************************************************

*******************************************************************************
"""

""" Imports 
*******************************************************************************
"""

import os
import requests
import time
import threading
import json
import serial
import serial.tools.list_ports
from MudMasterUI import globalErrorVar

""" Defines
*******************************************************************************
"""
deviceDescriptions = ['Arduino']




""" Functions
*******************************************************************************
"""

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


""" Classes
*******************************************************************************
"""

class MountingSystem_Manager(object):
    def __init__(self, app=None):
        """ @brief  Initialisation function for the mounting system manager.
            @param  None
            @retval None - Initialisation function.

        """
        self._app = None
        self._serialPort = None
        self._status = -1 # 0 = good, 1 = bad, -1 = not connected
        self._calibrated = False
        self._currentHeight = None
        self._lastMessageTime = None
        self._config_commands = None
        self._current_actuator = 0

        self._heightRange = {'min': None, 'max': None}

        self._commandQueue = []

        self._managementThreadRun = False
        
        self._lock = threading.Lock() # lock used to protect data when it is being changed.
        # start the management thread
        
        if(app != None):
            self.init_app(app)
        

    def init_app(self, app):
        """ @brief  App initialiser used for application factory structure.
            @param  app - reference to the application
            @retval None

        """
        self._app = app
        self._config_commands = self._app.config['CONFIG_SYSTEM'].get('mountingSystemCommands', {})
        self._config_limits = self._app.config['CONFIG_SYSTEM'].get('mountingSystem', {'actuator_max': 210, 'actuator_min': 0})  # defaults to 130 if there is no config
        

        if(self._serialPort == None):
            self.openSerial()


    """ Serial Communications
    ***********************************************************************
    """
    def openSerial(self):
        """ @brief  Attempts to find and open the serial port.
            @param  None
            @retval None

        """
        try:
            if(self._serialPort == None):
                availablePorts = findSerialPorts()
                if(len(availablePorts) >= 1):
                    # found the arduino
                    print('Found Arduino')
                    print(availablePorts)
                    self._serialPort = serial.Serial(port = availablePorts[0].device, 
                                                    baudrate = 9600, 
                                                    timeout = 1.0, 
                                                    bytesize = serial.EIGHTBITS)

                    self._serialNo = availablePorts[0].serial_number

                    print('Serial No.:', self._serialNo)
                    print('connected')
                    self._status = 0

        except Exception as e:
            print('Communication Error: permission. {}'.format(e))
            self._status = -1
            
    def closeSerial(self):
        """ Closes the serial port if it is open. """
        try:
            if self._serialPort is not None:
                if self._serialPort.is_open:
                    self._serialPort.close()
                    print('Serial port closed.')
                self._serialPort = None
                self._serialNo = None
                self._status = -1
        except Exception as e:
            print('Error closing serial port: {}'.format(e))
            self._status = 1
    

    """ General Control Functions
    ***********************************************************************
    """


    """ General Query Functions
    ***********************************************************************
    """

    def get_actuator_position(self):# change for testing 
        """ @brief  Gets the current actuator position.
            @param  None
            @retval Current actuator position
            
            was used for previous actuator only need 210mm position so just hard coded 

        """

        try:

            return 210

        except Exception as e:
            print(e)
            #print(msg)
            #return None
            return 210


    def get_status(self):
        """ @brief  Gets the current status of the mounting system.
            @param  None
            @retval Current status

        """
        self.ConnectionCheck()
        return self._status
    

    """ Functions added by Joshua Paterson for new actuator 
    ***********************************************************************
    """
    def fullyExtend(self):

        try:
            # Code that may raise an exception
            def write_read(x):
                self._serialPort.write(bytes(x,   'utf-8'))
                time.sleep(0.05)
                data = self._serialPort.readline()
                return   data

            num = self._config_commands['RSI PRO Extend']
            print(num)
            value   = write_read(num)
            globalErrorVar.ErrorFromActuatorReadWrite = False
            return "success"
        except Exception as e:
            # Handle the exception and print the error message
            print(f"An error occurred: {e}")
            globalErrorVar.ErrorFromActuatorReadWrite = True
            return "fail"
            self.closeSerial()
            self.openSerial()
            
        
    def fullyRetact(self):
        try:
            # Code that may raise an exception
            def write_read(x):
                self._serialPort.write(bytes(x,   'utf-8'))
                time.sleep(0.05)
                data = self._serialPort.readline()
                return   data

            num = self._config_commands['RSI PRO Retract']
            value   = write_read(num)
            globalErrorVar.ErrorFromActuatorReadWrite = False
            return "success"
        except Exception as e:
            # Handle the exception and print the error message
            print(f"An error occurred at fullyRetact: {e}")
            globalErrorVar.ErrorFromActuatorReadWrite = True
            self.closeSerial()
            self.openSerial()
            return "fail"

            
            
    def ApplyBrake(self):
        try:
            #self.openSerial()
            # Code that may raise an exception
            def write_read(x):
                #print("in try from fully retact")
                self._serialPort.write(bytes(x,   'utf-8'))
                time.sleep(0.05)
                data = self._serialPort.readline()
                return   data
            num = self._config_commands['RSI PRO Stop']
            value   = write_read(num)
            #print(value)
            globalErrorVar.ErrorFromActuatorReadWrite = False
            return "success"
        except Exception as e:
            # Handle the exception and print the error message
            print(f"An error occurred: {e}")
            globalErrorVar.ErrorFromActuatorReadWrite = True
            self.closeSerial()
            self.openSerial()
            return "fail"
        
    def ConnectionCheck(self):
        try:
            #self.openSerial()
            # Code that may raise an exception
            def write_read(x):
                #print("in try from fully retact")
                self._serialPort.write(bytes(x,   'utf-8'))
                time.sleep(0.05)
                data = self._serialPort.readline()
                return   data
            num = self._config_commands['RSI PRO Connection Check']
            value   = write_read(num)
            #print(value)
            globalErrorVar.ErrorFromActuatorReadWrite = False
            self._status = 0
            return "success"
        except Exception as e:
            # Handle the exception and print the error message
            print(f"An error occurred: {e}")
            globalErrorVar.ErrorFromActuatorReadWrite = True
            self.closeSerial()
            self.openSerial()
            
            return "fail"