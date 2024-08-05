"""
*******************************************************************************
@file   module_dataLogger.py
@author Scott Thomason
@date   30 Sep 2021
@brief  Used to log the measurement data so that it is ready for transmission.

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

from datetime import datetime

""" Defines
*******************************************************************************
"""

""" Functions
*******************************************************************************
"""



""" Classes
*******************************************************************************
"""

class DataLogger(object):
    def __init__(self, app=None):
        """ @brief  Initialisation function for the mounting system manager.
            @param  None
            @retval None - Initialisation function.

        """
        # only need config data specifically for the data logger

        self._dataQueue = []
        self._measurementCount = 0

        self._managementThreadRun = True
        
        self._lock = threading.Lock() # lock used to protect data when it is being changed.

        if(app != None):
            self.init_app(app)


    def init_app(self, app):
        """ @brief  Initialises the VNA manager. 
            @param  app - the flask app object
            @retval None

        """
        self._app = app

        self.start_manager_thread()

    
    def start_manager_thread(self):
        """ @brief  Starts the fitting handler thread if the a reference to the application and database exist.
            @param  None
            @retval None

        """
        if(self._app != None):

            self._processThread = threading.Thread(target = self.managementThread)
            self._processThread.start()


    
    """ Interaction Functions
    ***********************************************************************
    """
    def uploadData(self, dataDict):
        """ @brief  Adds the dataDict to the data queue. This will be 
                    processed by the management thread. If no datetime info 
                    is included, this will be added.

                    GPS data isn't needed. It will be matched up at the server side based on the time.

            @param  dataDict - {year, month, day, hour, minute, second, tzinfo, density, moisture, measurementData: {freq, amplitude, phase, e', e''}}
            @retval None

        """
        
        now = datetime.utcnow()
        # add the datetime info if it isn't in there
        if 'year' not in dataDict:
            dataDict['year'] = now.year
            
        if 'month' not in dataDict:
            dataDict['month'] = now.month
            
        if 'day' not in dataDict:
            dataDict['day'] = now.day
            
        if 'hour' not in dataDict:
            dataDict['hour'] = now.hour
            
        if 'minute' not in dataDict:
            dataDict['minute'] = now.minute
            
        if 'second' not in dataDict:
            dataDict['second'] = now.second
            
        if 'tzinfo' not in dataDict:
            dataDict['tzinfo'] = now.tzinfo or 0 # 0 = utc

        self._lock.acquire()
        self._dataQueue.append(dataDict)
        self._lock.release()


    def saveData_measurement(dataDict, dataFormat, fileName):
        """ @brief  Formats the measurement data as a comma separate string.
            @param  dataDict - data to join
                    dataFormat - list of parameters that are needed
                    fileName - structured file name
            @retval csv data

        """
        with open(fileName, 'w') as outFile:
            outFile.write(','.join(dataFormat) + ',\n')
            outFile.write(','.join([dataDict[param] for param in dataFormat]) + ',\n')


    def saveData_vna(dataDict, dataFormat, fileName):
        """ @brief  Formats the vna data as a comma separate string.
            @param  dataDict - data to join
                    dataFormat - list of parameters that are needed
                    fileName - structured file name
            @retval csv data

        """
        with open(fileName, 'w') as outFile:
            outFile.write(','.join(dataFormat) + ',\n')
            for line in dataDict['measurementData']:
                outFile.write(','.join([line[param] for param in dataFormat]) + ',\n')

    
    """ Module Thread
    ***********************************************************************
    """

    def managementThread(self):
        """ @brief  This thread runs the data logger. It will periodically 
                    check for new data in the queue and store this in the 
                    machine's OneDrive directory. 
            @param  None
            @retval None

        """
        # initial setup

        print('data logging thread start')
        tmpData = None
        
        # while loop
        while(self._managementThreadRun):
            # first check for any new data
            
            if(len(self._dataQueue) > 0):
                # we have data, so pop the first one and process it
                self._lock.acquire()
                tmpData = self._dataQueue.pop()
                self._lock.release()

                print(tmpData)

                filePrefix = '{}{}{}_{}{}{}'.format(tmpData['datetime']['year'], tmpData['datetime']['month'], tmpData['datetime']['day'], tmpData['datetime']['hour'], tmpData['datetime']['minute'], tmpData['datetime']['second'])

                print(filePrefix)

                # first save the measurement data
                self.saveData_measurement(
                    tmpData, 
                    self._app.config['CONFIG_SYSTEM']['dataLogger']['headings_measurement'], 
                    os.path.join(
                        self._app.config['CONFIG_SYSTEM']['dataLogger']['saveLocation'], 
                        self._app.config['CONFIG_SYSTEM']['dataLogger']['baseFileName_measurement'].format(filePrefix)
                        )
                    )

                # save the VNA data
                self.saveData_vna(
                    tmpData, 
                    self._app.config['CONFIG_SYSTEM']['dataLogger']['headings_vna'], 
                    os.path.join(
                        self._app.config['CONFIG_SYSTEM']['dataLogger']['saveLocation'], 
                        self._app.config['CONFIG_SYSTEM']['dataLogger']['baseFileName_vna'].format(filePrefix)
                        )
                    )

            time.sleep(0.2)
