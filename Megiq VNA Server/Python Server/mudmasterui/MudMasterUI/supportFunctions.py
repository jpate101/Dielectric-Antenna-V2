"""
*******************************************************************************
@file   supportFunctions.py
@author Scott Thomason
@date   26 Apr 2022
@brief  Support functions for the system.

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
import time
import json
import cmath
import skrf as rf

""" Defines
*******************************************************************************
"""


""" Functions
*******************************************************************************
"""

def create_directories(app):
    """ @brief  Creates any missing directories.
        @param  app - application instance
        @retval None

    """
    if not os.path.exists(app.config['MACHINE_DIRECTORY']):
        print('Making machine directory')
        os.makedirs(app.config['MACHINE_DIRECTORY'])

    if not os.path.exists(app.config['CONFIG_DIRECTORY']):
        print('Making config directory')
        os.makedirs(app.config['CONFIG_DIRECTORY'])

    if not os.path.exists(app.config['CONFIG_DIRECTORY_VNA_CAL']):
        print('Making vna cal config directory')
        os.makedirs(app.config['CONFIG_DIRECTORY_VNA_CAL'])


def load_run_config(app):
    """ @brief:  Loads the run configuration from the config file.
        @param:  app: The application instance.
        @retval: The run configuration.
    
    """
    # checks if the config file exits, and loads it into the config_run variable, if it doesn't exist, it creates it
    if not os.path.exists(app.config['CONFIG_FILE_RUN']):
        print('Creating run config file')
        with open(app.config['CONFIG_FILE_RUN'], 'w') as f:
            json.dump(app.config['CONFIG_RUN'], f)

    # loads the config file into the config_run variable
    with open(app.config['CONFIG_FILE_RUN'], 'r') as f:
        # combine the loaded dictionary with the current one, overwriting any existing keys
        app.config['CONFIG_RUN'] = {**app.config['CONFIG_RUN'], **json.load(f)}


def save_run_config(app):
    """ @brief:  Saves the run configuration to the config file.
        @param:  app: The application instance.
        @retval: None
    
    """
    # save the config file
    with open(app.config['CONFIG_FILE_RUN'], 'w') as f:
        json.dump(app.config['CONFIG_RUN'], f)



def save_s11_data(filename, directory, datadict):
    """ @brief  Saves the S11 data to a file. Uses the skrf library to save the data as a touchstone file.
        @param  filename - the filename to save the data to
        @param  directory - the directory to save the data to
        @param  datadict - the data to save
        @retval None

    """
    # create a network using the data
    ntwk = rf.Network(f=datadict['frequency'], s=datadict['S11R'] + 1j*datadict['S11I'], f_unit='Hz')
    # save the data
    ntwk.write_touchstone(filename=filename, dir=directory)


def save_measurement_data(filename, datadict, headers):
    """ @brief:  Saves the measurement data to a csv file.
        @param:  filename - the filename to save the data to
        @param:  datadict - the data to save
        @param:  headers - the headers to use for the csv file
        @retval: None
    
    """
    # check that the file ends with .csv, if not add it
    if not filename.endswith('.csv'):
        filename += '.csv'

    # create a list of the data
    data = [datadict[key] for key in headers]
    # create a string of the data
    data_string = ','.join(map(str, data))
    #added due to ' being written in csv file 
    data_string = data_string.replace("'", "")
    #print(data_string)
    # append the data to the file
    with open(filename, 'a') as f:
        f.write(data_string + '\n')


""" Models for water and density
*******************************************************************************
"""

def model_water_percentage(permittivity, gradient_value, intercept_value):
    """ @brief:  Model used to calculate the percentage of water in the material.
        @param:  permittivity: The permittivity of the material.
        @param:  gradient_value: The gradient of the line for the model.
        @param:  intercept_value: The intercept of the line for the model.
        @retval: The percentage of water in the material.
    
    """
    return (permittivity - intercept_value) / gradient_value


def model_density(water_percentage, G, gamma_w, S):
    """ @brief:  Model used to calculate the density of the material.
        @param:  water_percentage: The percentage of water in the material.
        @param:  G: The conductivity of the material.
        @param:  gamma_w: The conductivity of water.
        @param:  S: The specific heat of the material.
        @retval: The density of the material.
    
    """
    w = water_percentage / 100
    temp = 1 + w*G/S
    return G * gamma_w / temp