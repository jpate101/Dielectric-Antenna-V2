"""
*******************************************************************************
@file   module_measurement_manager.py
@author Scott Thomason, Joshua Paterson 
@date   03 May 2022
@brief  Module used to manage the measurement process. This will interface with 
        the VNA manager to get the data and then process it. Also uses a finite 
        state machine to switch between the idle, calibration and measurement 
        states.

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
import numpy as np
import scipy.io
import cmath
import skrf.io
import skrf as rf
import datetime
from copy import deepcopy
from MudMasterUI.supportFunctions import *
from MudMasterUI.teltonikaSupportFunctions import *
from MudMasterUI import globalErrorVar


import random



""" Defines
*******************************************************************************
"""
state_list = ['idle', 'calibration', 'measurement']

testing = False



""" Classes
*******************************************************************************
"""
class Measurement_Manager(object):
    def __init__(self, app=None):
        """ @brief  Initialisation function for the measurement manager.
            @param  None
            @retval None - Initialisation function.

        """
        self._current_state = 'idle'
        self._current_measurement_data = {
            'site': None,
            'measurment_date': None,
            'vna_data': None, 
            'actuator_extension': None,
            'permittivity': None, 
            'water_percentage': None, 
            'density': None,
            'vna_filename': None,
            }

        self._next_measurement_time = 0

        self._current_calibration_position = -1  # set the current calibration position to -1 to indicate that the calibration is not complete
        self._save_data_directory = {
            'main': None,
            'calData': None, 
            'vnaData': None
            }

        self._measurement_file = None

        self._managementThreadRun = True
        
        if(app != None):
            self.init_app(app)


    def init_app(self, app, mounting_system, vna, dielectric_manager):
        """ @brief  Initialises the VNA manager. 
            @param  app - the flask app object
            @retval None

        """
        self._app = app
        self._mounting_system = mounting_system
        self._vna = vna
        self._dielectric_manager = dielectric_manager
        self._calibration_positions = list(range(self._app.config['CONFIG_SYSTEM']['mountingSystem']['actuator_min'], self._app.config['CONFIG_SYSTEM']['mountingSystem']['actuator_max'] + self._app.config['CONFIG_SYSTEM']['calibrationStep'], self._app.config['CONFIG_SYSTEM']['calibrationStep']))

        # make a dictionary of the calibration positions, the position is the key and the value is a dictionary of {'status': 0}
        self._calibration_status = {}

        for position in self._calibration_positions:
            # status: 0 - not measured, 1 - measuring, 2 - measured
            self._calibration_status[position] = 0

        # iterate over the dielectric_manager_positions and set the self._calibration_status for these to 2
        print('Current calibration data: ', self._dielectric_manager.get_calibration_positions())
        for position in self._dielectric_manager.get_calibration_positions():
            self._calibration_status[position] = 2

        print('calibrating steps: ', self._calibration_positions)

        self._current_measurement_status = 0  # 0 - waiting, 1 - measuring

        # load the current site from the app.config 
        self._current_measurement_data['site'] = self._app.config['CONFIG_RUN']['site']

        self.start_manager_thread()

    
    def start_manager_thread(self):
        """ @brief  Starts the fitting handler thread if the a reference to the application and database exist.
            @param  None
            @retval None

        """
        if(self._app != None):

            self._processThread = threading.Thread(target = self.managementThread)
            self._processThread.start()


    """ Functions
    *******************************************************************************
    """
    def set_site(self, site):
        """ @brief  Sets the current site of the measurement manager. This is the 
                    mine site that the machine is operating at.
            @param  site - the mine site that the machine is currently operating at
            @retval None

        """
        self._current_measurement_data['site'] = site


    def get_calibration_progress(self):
        """ @brief  This function will return the current calibration progress.
            @param  None
            @retval None

        """
        status = 'idle'

        if self._current_state == 'calibration':
            # if any of the calibration status is not 2 then the calibration is not complete
            if any(self._calibration_status[key] != 2 for key in self._calibration_status):
                status = 'calibrating'
            else:
                status = 'complete'

        # set status to complete if all calibration positions in the calibration status dictionary have a value of 2
        if all(value == 2 for value in self._calibration_status.values()):
            status = 'complete'
            

        return {'progress': self._calibration_status, 'status': status}


    def get_measurement_display_data(self):
        """ @brief  This function will return the current measurement display data.
            @param  None
            @retval None

        """
        data_dict = {}
        data_dict['site'] = self._app.config['SITE_CONFIG'][self._current_measurement_data['site']]['name']
        data_dict['measurement_date'] = self._current_measurement_data['measurment_date']
        data_dict['actuator_extension'] = self._current_measurement_data['actuator_extension'] or 0
        data_dict['permittivity'] = self._current_measurement_data['permittivity'] or 0
        data_dict['water_percentage'] = self._current_measurement_data['water_percentage'] or 0
        data_dict['density'] = self._current_measurement_data['density'] or 0
        data_dict['status'] = self._current_measurement_status
        data_dict['next_measurement_seconds'] = round(self._next_measurement_time - time.monotonic())  # no. of seconds until the next measurement

        return data_dict



    """ State Control Functions
    *******************************************************************************
    """
    def set_idle(self):
        """ @brief  This function will set the state to idle.
            @param  None
            @retval True - the state was set to idle. False - the state was not set to idle.

        """
        return self.set_state('idle')


    def run_calibration(self):
        """ @brief  This function will start the calibration process.
            @param  None
            @retval True - the calibration process was started. False - the calibration process was not started.

        """
        return self.set_state('calibration')


    def clear_calibration(self):
        """ @brief  This function will clear the calibration data.
            @param  None
            @retval None

        """
        self._current_calibration_position = -1  # set the current calibration position to -1 to indicate that the calibration is not complete
        self._dielectric_manager.clear_calibration_data()


    def start_measurement(self):
        """ @brief  This function will start the measurement process.
            @param  None
            @retval True - the measurement process was started. False - the calibration hasn't been performed.

        """
        # tell the dielectric manager to save the current calibration data
        self._save_data_directory['main'] = os.path.join(*[self._app.config['MACHINE_DIRECTORY'], 'vnaTouchstones', datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")])
        self._save_data_directory['calData'] = os.path.join(self._save_data_directory['main'], 'calData')
        self._save_data_directory['vnaData'] = os.path.join(self._save_data_directory['main'], 'vnaData')
        
        # make the directories
        if not os.path.exists(self._save_data_directory['main']):
            os.makedirs(self._save_data_directory['main'])

        if not os.path.exists(self._save_data_directory['calData']):
            os.makedirs(self._save_data_directory['calData'])

        if not os.path.exists(self._save_data_directory['vnaData']):
            os.makedirs(self._save_data_directory['vnaData'])

        print('saving calibration data to: ', self._save_data_directory['calData'])
        self._dielectric_manager.save_calibration_data(self._save_data_directory['calData'])

        # create the measurment file
        self._measurement_file = os.path.join(self._app.config['MACHINE_DIRECTORY'], self._app.config['CONFIG_SYSTEM']['dataLogger']['baseFileName_measurement'].format(datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")))
        print('saving measurement data to: ', self._measurement_file)

        # add the headers to the measurement file
        with open(self._measurement_file, 'w') as f:
            f.write(','.join(self._app.config['CONFIG_SYSTEM']['dataLogger']['headings_measurement']) + '\n')

        return self.set_state('measurement')


    def set_state(self, state):
        """ @brief  Sets the current state of the measurement manager.
            @param  state - the state to set
            @retval None

        """
        if state == 'measurement':
            if self._dielectric_manager.is_calibrated() == True or testing == True:
                self._current_state = state
            
            else:
                return False

        else:
            self._current_state = state

        return True



    """ State Functions
    *******************************************************************************
    """
    def idle_state(self):
        """ @brief  This state is used to wait for a command to start the 
                    measurement.
            @param  None
            @retval None

        """
        time.sleep(self._app.config['CONFIG_RUN']['measurement_manager']['idle_sleep_time'])

    
    def calibration_state(self, testing=False):
        """ @brief  This state is used to calibrate the system. This will 
                    instruct the actuator to move to the next position in the 
                    list. For each position, it will get a measurement from the 
                    VNA and save that to the dielectric calibration module.
            @param  None
            @retval None

        """
        print('measurement system  calibration')
        # reset all of the calibration status to 0
        self._calibration_status = {position: 0 for position in self._calibration_status}

        # iterate over the calibration positions, for each position, move the actuator, then get a measurement and pass it to the calibration module
        for position in self._calibration_positions:
            self._calibration_status[position] = 1
            if testing == False:
                try:
                    self._mounting_system.set_actuator(position)
                    # wait for the actuator to move to that position, checking the current position, relative to the expected
                    time.sleep(0.5)
                    break_out_count = 0
                    while(abs(self._mounting_system.get_actuator_position() - position) > self._app.config['CONFIG_SYSTEM']['mountingSystem']['actuator_tolerance']):
                        time.sleep(0.1)
                        break_out_count += 1
                        if(break_out_count > 1):
                            print('measurement system  calibration error - actuator not moving')
                            break

                    calibration_position = self._mounting_system.get_actuator_position()
                    print('measurement system  calibration position: ', calibration_position)

                    # get the measurement from the VNA
                    s11_data = self._vna.get_nextData(forNN=True)

                    # add the calibration measurement to the calibration module - using the desired position as the input position
                    self._dielectric_manager.add_calibration_measurement(position, s11_data)

                except Exception as e:
                    print('measurement system  calibration error - ', e)
                    self._calibration_status[position] = 0
                    calibration_position = position

                self._current_calibration_position = calibration_position
                self._calibration_status[position] = 2

                time.sleep(0.1)

            else:
                time.sleep(2)
                self._current_calibration_position = position
                self._calibration_status[position] = 2

        # now move the actuator back to 0 and return to the idle state
        self._mounting_system.set_actuator(0)
        self._current_state = 'idle'
        
    


    def measurement_state(self, testing=False):
        """ @brief  This state is used to take a measurement from the VNA.
            @param  None
            @retval None

        """
        
        now = time.monotonic()

        # check if enough time has passed since the last measurement
        if(now >= self._next_measurement_time):
            print("measurement_state")
            self._current_measurement_status = 1
            
            testing = False #added of testing


            if testing == False:
                # get the measurement from the VNA
                self._current_measurement_data['vna_data'] = self._vna.get_nextData(forNN=True)
                self._current_measurement_data['actuator_extension'] = self._mounting_system.get_actuator_position() # here is the string to float issue/error log 

                #print("here 2")
                # use the calibration module to convert the S11 data to permittivity
                self._current_measurement_data['permittivity'] = self._dielectric_manager.convert_to_permittivity(self._current_measurement_data['vna_data'], self._current_measurement_data['actuator_extension'])
                #print("here 2.1")
                # now calculate the water percentage and density using the site config and current site
                # check if the current site is in the list of sites, otherwise use the default site
                if self._current_measurement_data['site'] in self._app.config['SITE_CONFIG']:
                    site_config = self._app.config['SITE_CONFIG'][self._current_measurement_data['site']]
                else:
                    site_config = self._app.config['SITE_CONFIG']['default']

                self._current_measurement_data['water_percentage'] = site_config['model_water'](self._current_measurement_data['permittivity'])
                self._current_measurement_data['density'] = site_config['model_density'](self._current_measurement_data['water_percentage'])
                
                #added teltonika readings 
                login_endpoint()
                latLong = get_GPS_data_endpoint()
                #print("\n")
                print(latLong)
                #print("\n")
                self._current_measurement_data['latitude'] = latLong['latitude']
                self._current_measurement_data['longitude'] = latLong['longitude']

                # set the current datetime for the measurement
                self._current_measurement_data['measurment_date'] = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")  # current universal coordinated time

                # save the measurement 
                # vna data needs to be saved as a touchstone file
                # everything else should be saved as a csv file

                # make the filename for the vnaData, this needs the current datetime, actuator extension and vnaData in the name
                vna_filename = self._app.config['CONFIG_SYSTEM']['dataLogger']['baseFileName_vna'].format(self._current_measurement_data['measurment_date'].replace(':', '-') + '_' + str(self._current_measurement_data['actuator_extension']))
                save_s11_data(vna_filename, self._save_data_directory['vnaData'], self._current_measurement_data['vna_data'])


                self._current_measurement_data['vna_filename'] = vna_filename
                # now save the remaining data as a csv file in the main directory
                #measurement_data_filename = self._app.config['CONFIG_SYSTEM']['dataLogger']['baseFileName_measurement'].format(self._current_measurement_data['measurment_date'].replace(':', '-') + '_' + str(self._current_measurement_data['actuator_extension']))
                save_measurement_data(self._measurement_file, self._current_measurement_data, self._app.config['CONFIG_SYSTEM']['dataLogger']['headings_measurement'])


                self._current_measurement_status = 0

            else:
                # fake measurement data
                print(" in measurement state - fake reading taken/in csv")
                self._current_measurement_data['measurment_date'] = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
                self._current_measurement_data['permittivity'] = random.randrange(40, 60)
                self._current_measurement_data['water_percentage'] = random.randrange(0, 100)
                self._current_measurement_data['density'] = random.randrange(0, 20)
                self._current_measurement_data['actuator_extension'] = self._mounting_system.get_actuator_position()
                
                login_endpoint()
                latLong = get_GPS_data_endpoint()
                print("\n")
                print(latLong)
                print("\n")
                self._current_measurement_data['latitude'] = latLong['latitude']
                self._current_measurement_data['longitude'] = latLong['longitude']
                
                # make the filename for the vnaData, this needs the current datetime, actuator extension and vnaData in the name
                save_measurement_data(self._measurement_file, self._current_measurement_data, self._app.config['CONFIG_SYSTEM']['dataLogger']['headings_measurement'])

                self._current_measurement_status = 0

            self._next_measurement_time = now + self._app.config['CONFIG_RUN']['measurement_manager']['measurement_delay']#the reason it take 30second before nex measurement 

    """ Module Thread that joshua paterson added for RSI PRO mount 
    ***********************************************************************
    """


    def calibration_state_MV2(self, testing=False):
        """ @brief  This state is used to take a a calibration reading at 210mm.
            @param  None
            @retval None

        """
        print('measurement system calibration at 210 mm MV2')
        globalErrorVar.CurrentlyCalibrating = True

        # Reset calibration status for all positions
        self._calibration_status = {position: 0 for position in self._calibration_status}

        # Calibrate at 210 mm position
        self._calibration_status[210] = 1

        if not testing:
            try:
                # Simulate actuator movement to 210 mm position (replace with actual implementation)
                time.sleep(0.5)
                calibration_position = 210
                print('measurement system calibration position:', calibration_position)

                # Simulate getting measurement data from VNA (replace with actual implementation)
                try:
                    s11_data = self._vna.get_nextData(forNN=True)
                except TimeoutError as e:
                    print('measurement system calibration error:', e)
                    self._calibration_status[210] = 0
                    calibration_position = 210
                    self._current_state = 'idle'
                    globalErrorVar.ErrorFromMeasurementManager = True
                    raise TimeoutError("Timeout occurred: 10 seconds elapsed while waiting for new data. from state_mv2")

                print("get_nextData")

                # Simulate adding calibration measurement to manager (replace with actual implementation)
                self._dielectric_manager.add_calibration_measurement(210, s11_data)
                print('Calibration done')

            except Exception as e:
                print('measurement system calibration error:', e)
                self._calibration_status[210] = 0
                calibration_position = 210

            self._current_calibration_position = calibration_position
            self._calibration_status[210] = 2

            time.sleep(0.1)

        else:
            time.sleep(2)
            self._current_calibration_position = 210
            self._calibration_status[210] = 2
            print('measurement system calibration position (Testing):', calibration_position)

        # Return actuator to 0 and transition to idle state (replace with actual implementation)
        # self._mounting_system.set_actuator(0)
        globalErrorVar.CurrentlyCalibrating = False
        self._current_state = 'idle'
        
    def measurement_state_MV2(self, testing=False):
        """ @brief  This state is used to take a measurement from the VNA when using the button from the home page.
            @param  None
            @retval None

        """
        try:
            now = time.monotonic()
            
            if(now >= self._next_measurement_time):
                
                print("measurement_state_MV2")
                
                self._next_measurement_time = now + self._app.config['CONFIG_RUN']['measurement_manager']['measurement_delay']#the reason it take 30second before nex measurement 
            
            
                # get the measurement from the VNA
                self._current_measurement_data['vna_data'] = self._vna.get_nextData(forNN=True)
                self._current_measurement_data['actuator_extension'] = self._mounting_system.get_actuator_position() # here is the string to float issue/error log 

                #print("here 2")
                    # use the calibration module to convert the S11 data to permittivity
                self._current_measurement_data['permittivity'] = self._dielectric_manager.convert_to_permittivity(self._current_measurement_data['vna_data'], self._current_measurement_data['actuator_extension'])
                #print("here 2.1")
                    # now calculate the water percentage and density using the site config and current site
                    # check if the current site is in the list of sites, otherwise use the default site
                if self._current_measurement_data['site'] in self._app.config['SITE_CONFIG']:
                    site_config = self._app.config['SITE_CONFIG'][self._current_measurement_data['site']]
                else:
                    site_config = self._app.config['SITE_CONFIG']['default']

                self._current_measurement_data['water_percentage'] = site_config['model_water'](self._current_measurement_data['permittivity'])
                self._current_measurement_data['density'] = site_config['model_density'](self._current_measurement_data['water_percentage'])
                    
                    #added teltonika readings 
                login_endpoint()
                latLong = get_GPS_data_endpoint()
                self._current_measurement_data['latitude'] = latLong['latitude']
                self._current_measurement_data['longitude'] = latLong['longitude']

                    # set the current datetime for the measurement
                self._current_measurement_data['measurment_date'] = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")  # current universal coordinated time

                    # save the measurement 
                    # vna data needs to be saved as a touchstone file
                    # everything else should be saved as a csv file

                    # make the filename for the vnaData, this needs the current datetime, actuator extension and vnaData in the name
                vna_filename = self._app.config['CONFIG_SYSTEM']['dataLogger']['baseFileName_vna'].format(self._current_measurement_data['measurment_date'].replace(':', '-') + '_' + str(self._current_measurement_data['actuator_extension']))
                save_s11_data(vna_filename, self._save_data_directory['vnaData'], self._current_measurement_data['vna_data'])
                
                
                self._current_measurement_data['vna_filename'] = vna_filename
                    # now save the remaining data as a csv file in the main directory
                    #measurement_data_filename = self._app.config['CONFIG_SYSTEM']['dataLogger']['baseFileName_measurement'].format(self._current_measurement_data['measurment_date'].replace(':', '-') + '_' + str(self._current_measurement_data['actuator_extension']))
                save_measurement_data(self._measurement_file, self._current_measurement_data, self._app.config['CONFIG_SYSTEM']['dataLogger']['headings_measurement'])
                
                print('---------Measurements taken---------')
            time.sleep(1)
        except Exception as e:
            # Handle other exceptions
            print(f"An error occurred: {e}")



    """ Module Thread
    ***********************************************************************
    """

    def managementThread(self):
        """ @brief  This thread runs the mounting system. It will send 
                    commands to set the height of the module and receive any 
                    data that has been sent back. 
            @param  None
            @retval None

        """
        # initial setup

        print('measurment system  thread start')

        # while loop
        while(self._managementThreadRun):

            # check the current state
            if(self._current_state == 'idle'):
                self.idle_state()

            elif(self._current_state == 'calibration'):
                self.calibration_state(testing=testing)
                time.sleep(0.1)
            elif(self._current_state == 'measurement_MV2'):#added by me //will prevent below if else statment from running and will also cause the measuremnt to dely on  self.measurement_state(testing=testing) as well  
                self.measurement_state_MV2()
                self._current_state = 'idle'
                # don't need the sleep, this is handled by the function

            elif(self._current_state == 'measurement'):
                self.measurement_state(testing=testing)
                # don't need the sleep, this is handled by the function
                pass

            else:
                print('measurement system  thread error')
                time.sleep(0.1)