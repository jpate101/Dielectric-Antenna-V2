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
import subprocess

import numpy as np

from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, send_from_directory, jsonify, make_response, abort, Blueprint, current_app, session

from MudMasterUI.mountingSystemV2 import bp  # Import Blueprint for mountingSystemV2
from MudMasterUI import controller_mountingSystem  # Import controller for mounting system operations
from MudMasterUI import measurement_manager  # Import measurement manager
from MudMasterUI import module_dielectric_manager
from MudMasterUI import globalErrorVar  # Import global error tracking

import MudMasterUI.config as ConfigFile

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
    )

@bp.route('/mounting-system-v2/Leave', methods=['GET'])
def Leave():
    """Stops any ongoing measurement when leaving the page."""
    global takeMeasurement
    takeMeasurement = False
    return jsonify({"message": "Leave Successful"})  

@bp.route('/mounting-system-v2/Measure', methods=['GET'])
def Measure():
    """Starts or stops the measurement thread based on the current state."""
    global takeMeasurement
    global isExtended
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
                time.sleep(38)  # Wait for the actuator to fully retract
                controller_mountingSystem.ApplyBrake()
                isExtended = 2
        globalErrorVar.CurrentlyRetracting = False
        return jsonify({"message": "Fully retracted"})
    
    except Exception as e:
        isExtended = 1
        return jsonify({"error": "Error while retracting", "message": "Unsuccessful"})


# Updated Dash IP with correct interface ID
DASH_IP = "fe80::ae1d:dfff:fe40:58a7%5"

def ping_dash():
    """Pings the Dash device and returns True if online."""
    try:
        result = subprocess.run(
            ["ping", "-n", "1", DASH_IP],
            capture_output=True, text=True, timeout=3
        )
        return "ms" in result.stdout
    except Exception:
        return False

def measurement_thread():
    """Thread function for handling measurement operations."""
    global takeMeasurement
    global isExtended
    globalErrorVar.CurrentlyLogging = True

    try:
        while takeMeasurement:
            if not ping_dash():
                print("[INFO] Dash not detected. Waiting...")
                time.sleep(5)
                continue

            print("[INFO] Dash detected. Preparing to start measurement...")

            if isExtended in [1, 2]:
                try:
                    print("[ACTION] Extending actuator...")
                    time.sleep(10)
                    globalErrorVar.CurrentlyExtending = True
                    controller_mountingSystem.fullyExtend()
                    time.sleep(38)
                    controller_mountingSystem.ApplyBrake()
                    isExtended = 3
                    globalErrorVar.CurrentlyExtending = False
                    print("[SUCCESS] Actuator fully extended.")
                except Exception as e:
                    isExtended = 1
                    print("[ERROR] Failed to extend actuator:", e)
                    continue

            measurement_manager.start_measurement()
            print("[INFO] Measurement started.")

            while takeMeasurement and ping_dash():
                measurement_manager._current_state = 'measurement_MV2'
                time.sleep(measurement_manager._app.config['CONFIG_RUN']['measurement_manager']['measurement_delay'])

                if globalErrorVar.ErrorFromMeasurementManager:
                    globalErrorVar.ErrorFromMeasurementManager = False
                    print("[WARNING] Measurement manager error encountered.")

                elif globalErrorVar.ErrorFromActuatorReadWrite or globalErrorVar.ErrorFromTeltonika:
                    print("[ERROR] Critical error from actuator or Teltonika. Stopping measurement.")
                    globalErrorVar.ErrorFromActuatorReadWrite = False
                    globalErrorVar.ErrorFromTeltonika = False
                    takeMeasurement = False
                    break

                shutdown_time = datetime.strptime(ConfigFile.Config.AUTO_SHUT_DOWN_TIME, '%H:%M').time()
                current_time = datetime.now().time()
                print(f"[TIME] Current time: {current_time} | Shutdown at: {shutdown_time}")

                if current_time >= shutdown_time:
                    print("[INFO] Auto shutdown time reached. Stopping measurement.")
                    takeMeasurement = False
                    break

            print("[ACTION] Retracting actuator...")
            fully_retract()
            isExtended = 1
            print("[SUCCESS] Actuator retracted.")

            time.sleep(5)

    except Exception as e:
        isExtended = 1
        print("[EXCEPTION] Measurement thread encountered an error:", e)

    globalErrorVar.CurrentlyLogging = False
    print("[INFO] Measurement thread has exited.")