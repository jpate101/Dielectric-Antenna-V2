"""
*******************************************************************************
@file   MudMasterUI.mountingSystem.routes.py
@author Scott Thomason, Joshua Paterson 
@date   02 Feb 2022
@brief  Routes for the mounting system module in the application. Handles 
        various operations such as calibration, measurement, and actuator control.

REFERENCE:

*******************************************************************************
    Functions
*******************************************************************************

*******************************************************************************
"""

""" Imports
*******************************************************************************
"""
import json
import time
import os
import threading

import numpy as np

from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, send_from_directory, jsonify, make_response, abort, Blueprint, current_app, session

from MudMasterUI.mountingSystemV2 import bp  # Import Blueprint for mountingSystemV2
from MudMasterUI import controller_mountingSystem  # Import controller for mounting system operations
from MudMasterUI import measurement_manager  # Import measurement manager
from MudMasterUI import module_dielectric_manager
from MudMasterUI import globalErrorVar  # Import global error tracking

""" Defines
*******************************************************************************
"""

""" Variables 
*******************************************************************************
"""
# Flag to control measurement operations
takeMeasurement = False

# State indicator for actuator: 1 = unknown, 2 = retracted, 3 = extended
isExtended = 1


""" Routes
*******************************************************************************
"""

@bp.route('/')
@bp.route('/HomeV2')
@bp.route('/Home')
@bp.route('/home')
def mounting_system():
    """Renders the home page for the mounting system module."""
    # Define a default measurement delay
    current_measurement_delay = 60  
    
    # Create a list of site configurations
    sites = list(
        {
            'id': key,
            'name': current_app.config['SITE_CONFIG'][key]['name'],
            'country': current_app.config['SITE_CONFIG'][key]['country'],
            'calibration_date': current_app.config['SITE_CONFIG'][key]['calibration_date']
        } for key in current_app.config['SITE_CONFIG'].keys()
    )
    
    # Set the measurement manager state to 'idle'
    measurement_manager._current_state = 'idle'
    
    # Render the home page template with the current settings
    return render_template(
        'mountingSystemV2/mounting_systemV2.html',
        title='Home',
        year=datetime.now().year,
        showFooter=True,
        measurement_delays=current_app.config['CONFIG_SYSTEM']['measurement_manager']['measurement_delay_list'],
        current_measurement_delay=current_app.config['CONFIG_RUN']['measurement_manager']['measurement_delay'],
        sites=sites,
    )

@bp.route('/mounting-system-v2/Leave', methods=['GET'])
def Leave():
    """Stops any ongoing measurement when leaving the page."""
    global takeMeasurement
    takeMeasurement = False
    return jsonify({"message": "Leave Successful"})  

# @bp.route('/mounting-system-v2/Calibrate', methods=['GET'])
# def Calibrate():
#     """Performs calibration by extending the actuator and starting calibration."""
#     global takeMeasurement
#     global isExtended
#     takeMeasurement = False
#     try:
#         if isExtended == 1 or isExtended == 2:
#             # Extend the actuator if it's not already extended
#             globalErrorVar.CurrentlyExtending = True
#             sleep = controller_mountingSystem.fullyExtend()
#             if sleep == "success":
#                 time.sleep(32)  # Wait for the actuator to fully extend
#                 sleep = controller_mountingSystem.ApplyBrake()
#                 isExtended = 3
#                 globalErrorVar.CurrentlyExtending = False
#         # Start calibration process
#         measurement_manager.calibration_state_MV2()
#         if globalErrorVar.ErrorFromMeasurementManager:
#             return jsonify({"error": "Timeout occurred", "message": "VNA timed out"})
#         globalErrorVar.ErrorFromMeasurementManager = False
#         isExtended = 3
#         return jsonify({"message": "Calibrated"})  
#     except TimeoutError as e:
#         isExtended = 1
#         return jsonify({"error": "Timeout occurred", "message": "VNA timed out"})
#     except Exception as e:
#         isExtended = 1
#         return jsonify({"error": "Error while calibrating", "message": "Unsuccessful"})

@bp.route('/mounting-system-v2/Measure', methods=['GET'])
def Measure():
    """Starts or stops the measurement thread based on the current state."""
    global takeMeasurement
    global isExtended
    if takeMeasurement:
        takeMeasurement = False
        return jsonify({"message": "Measurement thread stopped. No longer logging Measurements"})
    
    #try:
    #    module_dielectric_manager.load_model()
    #except Exception as e:
    #    print(f"An error occurred: {e}")
    
    try:
        # Start the measurement thread if it's not already running
        if not takeMeasurement:
            takeMeasurement = True
            threading.Thread(target=measurement_thread).start()
        
        return jsonify({"message": "Measurement thread started. Will start running measurements"})
    
    except Exception as e:
        isExtended = 1
        return jsonify({"error": "Error starting measurement", "message": "Unsuccessful"})

@bp.route('/mounting-system-v2/fullyRetract', methods=['GET'])
def fully_retract():
    """Fully retracts the actuator and applies the brake."""
    global isExtended
    global takeMeasurement
    takeMeasurement = False
    globalErrorVar.ErrorFromMeasurementManager = False
    try:
        if isExtended == 1 or isExtended == 3:
            # Retract the actuator if it's not already retracted
            globalErrorVar.CurrentlyRetracting = True
            sleep = controller_mountingSystem.fullyRetact()
            if sleep == "success":
                time.sleep(32)  # Wait for the actuator to fully retract
                controller_mountingSystem.ApplyBrake()
                isExtended = 2
        globalErrorVar.CurrentlyRetracting = False
        return jsonify({"message": "Fully retracted"})
    
    except Exception as e:
        isExtended = 1
        return jsonify({"error": "Error while retracting", "message": "Unsuccessful"})


def measurement_thread():
    """Thread function for handling measurement operations."""
    global takeMeasurement
    global isExtended
    globalErrorVar.CurrentlyLogging = True
    try:
        if isExtended == 1 or isExtended == 2:
            try:
                # Extend actuator if required
                globalErrorVar.CurrentlyExtending = True
                controller_mountingSystem.fullyExtend()
                time.sleep(32)
                controller_mountingSystem.ApplyBrake()
                isExtended = 3
                globalErrorVar.CurrentlyExtending = False
            except Exception as e:
                isExtended = 1
                pass
        
        measurement_manager.start_measurement()
        
        while takeMeasurement:
            measurement_manager._current_state = 'measurement_MV2'
            time.sleep(measurement_manager._app.config['CONFIG_RUN']['measurement_manager']['measurement_delay'])
            if globalErrorVar.ErrorFromMeasurementManager:
                globalErrorVar.ErrorFromMeasurementManager = False
                takeMeasurement = False
            elif globalErrorVar.ErrorFromActuatorReadWrite:
                globalErrorVar.ErrorFromActuatorReadWrite = False
                takeMeasurement = False
            elif globalErrorVar.ErrorFromTeltonika:
                globalErrorVar.ErrorFromTeltonika = False
                takeMeasurement = False
    except Exception as e:
        isExtended = 1
    globalErrorVar.CurrentlyLogging = False