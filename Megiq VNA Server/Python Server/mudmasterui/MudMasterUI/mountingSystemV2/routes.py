"""
*******************************************************************************
@file   MudMasterUI.mountingSystem.routes.py
@author Scott Thomason
@date   02 Feb 2022
@brief  Routes for the main section of the app.

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

from MudMasterUI.mountingSystemV2 import bp
from MudMasterUI import controller_mountingSystem
from MudMasterUI import measurement_manager
from MudMasterUI import globalErrorVar
#github desktop tes t

""" Defines
*******************************************************************************
"""

""" Variables 
*******************************************************************************
"""

takeMeasurement = False

isExtended = 1 #1 = dont know, 2 = retracted , 3 - extended




""" Routes
*******************************************************************************
"""
@bp.route('/HomeV2')
def mounting_system():
    """Renders the home page."""
    current_measurement_delay = 60  
    sites = list(
        {
            'id': key,
            'name': current_app.config['SITE_CONFIG'][key]['name'],
            'country': current_app.config['SITE_CONFIG'][key]['country'],
            'calibration_date': current_app.config['SITE_CONFIG'][key]['calibration_date']
        } for key in current_app.config['SITE_CONFIG'].keys()
    )
    return render_template(
        'mountingSystemV2/mounting_systemV2.html',
        title='Home V2',
        year=datetime.now().year,
        showFooter=True,
        current_actuator_position=controller_mountingSystem.get_actuator_target(),
        measurement_delays=current_app.config['CONFIG_SYSTEM']['measurement_manager']['measurement_delay_list'],
        current_measurement_delay=current_app.config['CONFIG_RUN']['measurement_manager']['measurement_delay'],
        sites = sites,
    )

@bp.route('/mounting-system-v2/Leave', methods = ['GET'])
def Leave():
    print('from leave page endpoint')
    global takeMeasurement
    takeMeasurement = False
    return jsonify({"message": "Leave Successful"})  

@bp.route('/mounting-system-v2/Calibrate', methods = ['GET'])
def Calibrate():
    global takeMeasurement
    global isExtended
    print("/mounting-system-v2/fullyExtend------------------")
    takeMeasurement = False
    try:
        if(isExtended == 1 or isExtended == 2 ):
            print("Actuator Extending")
            globalErrorVar.CurrentlyExtending = True
            sleep = controller_mountingSystem.fullyExtend()
            #sleep = "success"
            if(sleep == "success"):
                time.sleep(32)
                sleep = controller_mountingSystem.ApplyBrake()
                isExtended = 3
                globalErrorVar.CurrentlyExtending = False
                print("Actuator Extended")
        measurement_manager.calibration_state_MV2()# used to be change variable to calibration but now 
        if (globalErrorVar.ErrorFromMeasurementManager):
            globalErrorVar.ErrorFromMeasurementManager = False
            return jsonify({"error": "Timeout occurred", "message": "VNA timed out"})
        print(globalErrorVar.ErrorFromMeasurementManager)
        print("Done Calibrating from mount-system-V2 route")
        isExtended = 3
        return jsonify({"message": "Calibrated"})  
    except TimeoutError as e:
        isExtended = 1
        print(f"Timeout occurred during calibration: {e}")
        return jsonify({"error": "Timeout occurred", "message": "VNA timed out"})
    except Exception as e:
        isExtended = 1
        print(f"Exception during calibration: {e}")
        return jsonify({"error": "Error while calibrating", "message": "Unsuccessful"})
    

@bp.route('/mounting-system-v2/Measure', methods = ['GET'])
def Measure():
    global takeMeasurement
    global isExtended
    print("/mounting-system-v2/Measure------------------")
    if takeMeasurement:
            takeMeasurement = False
            return jsonify({"message": "Measurement thread stopped. No longer logging Measurements"})
            
    
    
    try:
        # Start the measurement thread if it's not already running
        if not takeMeasurement:
            takeMeasurement = True
            threading.Thread(target=measurement_thread).start()
        
        return jsonify({"message": "Measurement thread started. Will start running measurements"})
    
    except Exception as e:
        isExtended = 1
        print(f"Exception while starting measurement: {e}")
        return jsonify({"error": "Error starting measurement", "message": "Unsuccessful"})
        
        
    
    

    return jsonify({"message": "exit from Measure"})  

@bp.route('/mounting-system-v2/fullyRetract', methods = ['GET'])
def fully_retract():
    global isExtended
    global takeMeasurement
    print("/mounting-system-v2/fullyRetract---------------------")
    
    takeMeasurement = False
    globalErrorVar.ErrorFromMeasurementManager = False
    print(isExtended)
    try:
        
        if isExtended == 1 or isExtended == 3:
            print("Actuator Retracting")
            globalErrorVar.CurrentlyRetracting = True
            sleep = controller_mountingSystem.fullyRetact()
            #sleep = "success"
            print(sleep)
            if(sleep == "success"):
                time.sleep(32)
                controller_mountingSystem.ApplyBrake()
                isExtended = 2
                print("Actuator Retracted")
        globalErrorVar.CurrentlyRetracting = False
        return jsonify({"message": "Fully retracted"})
    
    except Exception as e:
        print(f"Exception during full retraction: {e}")
        isExtended = 1
        return jsonify({"error": "Error while retracting", "message": "Unsuccessful"})


def measurement_thread():
    global takeMeasurement
    global isExtended
    globalErrorVar.CurrentlyLogging = True
    try:
        if isExtended == 1 or isExtended == 2:
            try: 
                print("Actuator Extending")
                globalErrorVar.CurrentlyExtending = True
                controller_mountingSystem.fullyExtend()
                time.sleep(32)
                controller_mountingSystem.ApplyBrake()
                isExtended = 3
                globalErrorVar.CurrentlyExtending = False
                print("Actuator Extended")
            except Exception as e:
                isExtended = 1
                pass
        
        measurement_manager.start_measurement()
        
        while takeMeasurement:
            print('-----here from measurement_thread------------------------------------------------------------------------')
            print(takeMeasurement)
            print(measurement_manager._app.config['CONFIG_RUN']['measurement_manager']['measurement_delay'])
            measurement_manager._current_state = 'measurement_MV2'
            time.sleep(measurement_manager._app.config['CONFIG_RUN']['measurement_manager']['measurement_delay'])
            if (globalErrorVar.ErrorFromMeasurementManager):
                globalErrorVar.ErrorFromMeasurementManager = False
                print('-ErrorFromMeasurementManager in takemeasurement thread- likely timed out')
                takeMeasurement = False
            elif (globalErrorVar.ErrorFromActuatorReadWrite):
                globalErrorVar.ErrorFromActuatorReadWrite = False
                print('-globalErrorVar.ErrorFromActuatorReadWrite in takemeasurement thread-')
                takeMeasurement = False
            elif (globalErrorVar.ErrorFromTeltonika):
                globalErrorVar.ErrorFromTeltonika = False
                print('-globalErrorVar.ErrorFromTeltonika in takemeasurement thread-')
                takeMeasurement = False
        print('-----exit from measurement_thread------------------------------------------------------------------------')
    except Exception as e:
        isExtended = 1
        print(f"Exception in measurement thread: {e}")
    globalErrorVar.CurrentlyLogging = False