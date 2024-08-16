"""
*******************************************************************************
@file   interface_VNA.py
@author Scott Thomason, Joshua Paterson 
@date   30 Sep 2021
@brief  VNA interfacing class that uses the Python requests module to connect to 
        the VNA server and request data from it. This is run in a thread that 
        will periodically request data from the VNA. This is made available 
        through class functions.

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
import numpy
import cmath
import numpy as np
from copy import deepcopy
import time
import psutil
from MudMasterUI import globalErrorVar

import ctypes
import subprocess

""" Defines
*******************************************************************************
"""
update_config = False


""" Classes
*******************************************************************************
"""

class VNA_Manager(object):
    def __init__(self, app=None):
        """ 
        @brief  Initializes the VNA manager. 
        @param  app - Optional; the Flask application object for configuration.
        @retval None

        Initializes the VNA manager with default or provided configuration values. 
        Sets up data structures, flags, and starts the management thread.
        """
        
        self._measurementData = {}
        self._currentData = {'port1': {}, 'port2': {}, 'measurementCount': -1, 'sweepTime': 0}
        self._status = 0
        self._vnaStatus = {}
        self._vnaStatusTime = 0
        self._vnaInfo = {}
        self._mode = 0
        self._lastRequestedData = 0
        self._measuringFlag = False
        self._vnaProgram = None
        self._vnaServerActive = False
        self._managementThreadRun = True
        self._lock = threading.Lock()  # Protects data during concurrent access

        if app:
            self.init_app(app)

    def init_app(self, app):
        """ 
        @brief  Initializes the VNA manager with Flask application configuration.
        @param  app - the Flask application object.
        @retval None

        Configures the VNA manager with parameters from the Flask app configuration. 
        Checks for and manages the VNA server process.
        """
        
        self._app = app
        self._vnaIP = self._app.config['CONFIG_SYSTEM'].get('vnaIP', '127.0.0.1')
        self._vnaPort = self._app.config['CONFIG_SYSTEM'].get('vnaPort', 5000)
        self._updateInterval = self._app.config['CONFIG_SYSTEM'].get('vnaUpdateInterval', 0.5)
        self._statusInterval = self._app.config['CONFIG_SYSTEM'].get('vnaStatusInterval', 5)
        self._vnaRoutes = self._app.config['CONFIG_SYSTEM'].get('vnaRoutes', {})

        # Current and new configurations for the VNA
        self._config_current = {
            'frequency': {'min': None, 'max': None, 'step': None},
            'power': None,
        }
        self._config_new = self._app.config['CONFIG_SYSTEM'].get('vnaSettings', self._config_current)
        
        # Check if the VNA server is active
        self._vnaServerActive = self._app.config['CONFIG_SYSTEM'].get('vnaServerProcessName', 'MegiqVnaServer.exe') in (p.name() for p in psutil.process_iter())
        
        # Start VNA server if not active
        if not self._vnaServerActive:
            server_path = self._app.config['CONFIG_MACHINE'].get('vnaServerProcessPath', None)
            if server_path is None:
                print('WARNING: config file does not contain path to VNA server executable')
            else:
                # Terminate existing instances and start new server
                for p in psutil.process_iter():
                    if p.name() == self._app.config['CONFIG_SYSTEM'].get('vnaProgramName', 'MiQVNA.exe'):
                        p.terminate()

                self._run_as_admin(server_path)
                
                # Wait for the VNA program to start
                foundProgram = False
                self._vnaProgram = None
                while not foundProgram:
                    for p in psutil.process_iter():
                        if p.name() == self._app.config['CONFIG_SYSTEM'].get('vnaProgramName', 'MiQVNA.exe'):
                            foundProgram = True
                            self._vnaProgram = p
                            break

                print(self._vnaProgram)
                print('PID: ', self._vnaProgram.pid)
                print('NAME: ', self._vnaProgram.name())
                print('CMDLINE: ', self._vnaProgram.cmdline())
                print('PPID: ', self._vnaProgram.ppid())
                print('PGROUP: ', self._vnaProgram.parent())

        self.start_manager_thread()

    def start_manager_thread(self):
        """ 
        @brief  Starts the thread for managing VNA operations. 
        @param  None
        @retval None

        Creates and starts a new thread to handle VNA data management.
        """
        
        if self._app:
            self._processThread = threading.Thread(target=self.deviceManagementThread)
            self._processThread.start()

    """ VNA Communication Functions
    ***********************************************************************
    """
    def vna_webRequest(self, routeKey, data=None):
        """ 
        @brief  Makes an HTTP GET or POST request to the VNA server. 
        @param  routeKey - the route key for the request URL.
                data - Optional; data to be sent with the request.
        @retval dict - JSON response from the server or an empty dictionary if the request fails.
        """
        
        if not self._vnaServerActive:
            # Check if the server is running now
            self._vnaServerActive = self._app.config['CONFIG_SYSTEM'].get('vnaServerProcessName', 'MegiqVnaServer.exe') in (p.name() for p in psutil.process_iter())

        if self._vnaServerActive:
            urlData = f'http://{self._vnaIP}:{self._vnaPort}/{self._vnaRoutes[routeKey]["endpoint"]}'

            try:
                if self._vnaRoutes[routeKey]['method'] == 'GET':
                    msg = requests.get(url=urlData, data=data)
                else:
                    msg = requests.post(url=urlData, data=data)

                if msg.status_code == 200:
                    self._vnaServerActive = True
                    return msg.json()
            except Exception as e:
                print(e)
                print("-print to check if this is where the refused connection to VNA server is from-")
                self._vnaServerActive = False
            
        return {}

    """ Data Access Functions
    ***********************************************************************
    """
    def get_currentData(self, asJson=False, magPhase=False, forNN=False):
        """ 
        @brief  Retrieves the most recent data.
        @param  asJson - Optional; whether to return data as a JSON object.
                magPhase - Optional; whether to return magnitude and phase instead of real and imaginary parts.
                forNN - Optional; whether to format data for use in a neural network.
        @retval dict - The current data, formatted according to parameters.
        """
        
        # Lock and copy the current data to ensure safe access
        self._lock.acquire()
        dataCopy = deepcopy(self._currentData)
        self._lastRequestedData = self._currentData['measurementCount']
        self._lock.release()

        if asJson:
            # Convert complex numbers to JSON-compatible format
            for key in dataCopy['port1']:
                if not magPhase:
                    dataCopy['port1'][key] = {'real': dataCopy['port1'][key].real, 'imag': dataCopy['port1'][key].imag}
                else:
                    dataCopy['port1'][key] = {'mag': 10*np.log10(abs(dataCopy['port1'][key])), 'phase': cmath.phase(dataCopy['port1'][key])}

        if forNN:
            nnData = {'frequency': [], 'S11R': [], 'S11I': []}
            for key in dataCopy['port1']:
                nnData['frequency'].append(key)
                nnData['S11R'].append(dataCopy['port1'][key].real)
                nnData['S11I'].append(dataCopy['port1'][key].imag)

            nnData['frequency'] = np.array(nnData['frequency'])
            nnData['S11R'] = np.array(nnData['S11R'])
            nnData['S11I'] = np.array(nnData['S11I'])

            return nnData

        return dataCopy

    def get_nextData(self, asJson=False, magPhase=False, forNN=False):
        """ 
        @brief  Waits for and returns the next set of data.
        @param  asJson - Optional; whether to return data as a JSON object.
                magPhase - Optional; whether to return magnitude and phase.
                forNN - Optional; whether to format data for a neural network.
        @retval dict - The next set of data, formatted according to parameters.
        """
        
        startingMeasurement = self._currentData['measurementCount']
        start_time = time.time()
        timeout = 20  # Timeout period in seconds

        while (startingMeasurement == self._currentData['measurementCount'] and time.time() - start_time < timeout):
            time.sleep(0.1)

        if time.time() - start_time >= timeout:
            print('Timeout waiting for new measurement')
            return {}

        return self.get_currentData(asJson=asJson, magPhase=magPhase, forNN=forNN)

    def get_measurementData(self, asJson=False, magPhase=False):
        """ 
        @brief  Retrieves the entire set of measurement data.
        @param  asJson - Optional; whether to return data as a JSON object.
                magPhase - Optional; whether to return magnitude and phase.
        @retval dict - The measurement data, formatted according to parameters.
        """
        
        if asJson:
            for key in self._measurementData:
                if not magPhase:
                    self._measurementData[key] = {'real': self._measurementData[key].real, 'imag': self._measurementData[key].imag}
                else:
                    self._measurementData[key] = {'mag': 10*np.log10(abs(self._measurementData[key])), 'phase': cmath.phase(self._measurementData[key])}

        return self._measurementData

    def get_vnaStatus(self):
        """ 
        @brief  Retrieves the current status of the VNA. 
        @param  None
        @retval dict - The VNA status.
        """
        
        return self._vnaStatus

    def get_vnaInfo(self):
        """ 
        @brief  Retrieves information about the VNA. 
        @param  None
        @retval dict - Information about the VNA.
        """
        
        return self._vnaInfo

    def get_vnaConfig(self):
        """ 
        @brief  Retrieves the current configuration of the VNA. 
        @param  None
        @retval dict - The VNA configuration.
        """
        
        return self._config_current

    def update_vnaConfig(self, config):
        """ 
        @brief  Updates the VNA configuration. 
        @param  config - Dictionary containing the new configuration values.
        @retval None

        Updates the VNA configuration with the provided values and requests the VNA server to apply these settings.
        """
        
        self._config_new = config
        self._request_vnaConfig()

    def _request_vnaConfig(self):
        """ 
        @brief  Requests the VNA server to update its configuration. 
        @param  None
        @retval None
        
        Sends the new configuration settings to the VNA server. If successful, updates the current configuration.
        """
        
        self._lock.acquire()
        config = self._config_new
        self._lock.release()
        
        if config:
            response = self.vna_webRequest('vnaUpdateConfig', json.dumps(config))
            if response:
                self._config_current = config

    """ Thread Management Functions
    ***********************************************************************
    """
    def deviceManagementThread(self):
        """ 
        @brief  Manages the VNA device operations in a separate thread. 
        @param  None
        @retval None

        Periodically requests data from the VNA and updates internal data structures. Handles VNA status updates.
        """
        
        while self._managementThreadRun:
            try:
                if self._vnaServerActive:
                    self._check_vnaStatus()
                    if update_config:
                        self._request_vnaConfig()
                        update_config = False

                    # Fetch the latest measurement data
                    response = self.vna_webRequest('vnaMeasurementData')
                    if response:
                        self._measurementData = response
                        self._currentData['measurementCount'] = self._measurementData.get('measurementCount', -1)
                        self._currentData['sweepTime'] = self._measurementData.get('sweepTime', 0)
                    
                time.sleep(self._updateInterval)
                
            except Exception as e:
                print(f'Error in deviceManagementThread: {e}')
                self._vnaServerActive = False
                time.sleep(self._updateInterval)

    def _check_vnaStatus(self):
        """ 
        @brief  Checks and updates the VNA status.
        @param  None
        @retval None
        
        Requests the VNA server for its current status and updates the internal status information.
        """
        
        response = self.vna_webRequest('vnaStatus')
        if response:
            self._vnaStatus = response
            self._vnaStatusTime = time.time()

    def stop_manager_thread(self):
        """ 
        @brief  Stops the VNA management thread. 
        @param  None
        @retval None
        
        Signals the management thread to stop and waits for it to terminate.
        """
        
        self._managementThreadRun = False
        if self._processThread.is_alive():
            self._processThread.join()

    def _run_as_admin(self, program):
        """ 
        @brief  Runs a program with administrative privileges. 
        @param  program - The path to the program executable.
        @retval None
        
        Executes the specified program with administrative privileges. This is typically used to start the VNA server.
        """
        
        try:
            if os.name == 'nt':  # Windows only
                ctypes.windll.shell32.ShellExecuteW(None, 'runas', program, None, None, 1)
            else:
                # If not Windows, attempt to use sudo
                subprocess.Popen(['sudo', program], shell=False)
        except Exception as e:
            print(f"Failed to run program as admin: {e}")      
                




if __name__ == '__main__': 
    # library test code
    from config import config_system
    vna = VNA_Manager(config_system)

