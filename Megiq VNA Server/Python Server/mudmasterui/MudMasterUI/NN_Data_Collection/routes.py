"""
*******************************************************************************
@file   routes.py
@author Joshua Paterson 
@date   02 Feb 2022
@brief  Routes for the mounting system module in the application. Handles 
        various operations such as calibration, measurement, and actuator control.
        
        
no longer works due to removeal of VNA touchstones folder 

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

from MudMasterUI import measurement_manager  # Import measurement manager
from MudMasterUI import globalErrorVar

from MudMasterUI import Config
import shutil  

from . import bp  # Import the blueprint

""" Routes
*******************************************************************************
"""

@bp.route('/NN_Data_Collect')
def collect_data():
    """Renders the home page for the mounting system module."""
    return render_template(
        'NN_Data_Collection/nn_data_collection.html',
        title='NN Data',
        year=datetime.now().year,
        showFooter=True,
    )
    
    
@bp.route('/submit_label', methods=['POST'])
def submit_label():
    data = request.get_json()  # Get the JSON data from the request
    label = data.get('label')   # Extract the 'label' field

    # Check if the label can be converted to a float
    try:
        float_value = float(label)  # Attempt to convert to float
    except ValueError:
        return jsonify(message="Invalid input: Please enter a valid float."), 400
    
    

    # Define the base folder path
    base_folder_path = r'C:\Users\JoshuaPaterson\Downloads\Testing3'  # Use raw string

    # Create a new folder with a timestamp or unique identifier
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    new_folder_path = os.path.join(base_folder_path, f'data_{timestamp}')

    # Create the new folder
    os.makedirs(new_folder_path, exist_ok=True)

    # Define the path for the JSON file
    file_path = os.path.join(new_folder_path, 'data.json')
    
    globalErrorVar.NN_Data_Collection_File_path = new_folder_path
    
    try:
        measurement_manager.measurement_state_MV3()
    except ValueError:
        return jsonify(message="ERROR with VNA"), 400
    
    if (globalErrorVar.ErrorFromMeasurementManager == True):
        globalErrorVar.ErrorFromMeasurementManager = False
        return jsonify(message="ERROR with VNA"), 400

    # Write the float value to a JSON file
    with open(file_path, 'w') as json_file:
        json.dump({'label': float_value}, json_file)
        
    

    return jsonify(message=f"You entered a valid float: {float_value}. Data saved to {new_folder_path}")


    
@bp.route('/submit_label_v2', methods=['POST'])
def submit_label_v2():
    data = request.get_json()
    label = data.get('label')
    shear_vain_20cm = data.get('shearVain20cm')
    shear_vain_50cm = data.get('shearVain50cm')
    shear_vain_80cm = data.get('shearVain80cm')  
    surface_label = data.get('surfaceLabel')
    height_Label = data.get('heightLabel')
    

    # Validate the label input
    try:
        float_value = float(label)
    except ValueError:
        return jsonify(message="Invalid input: Please enter a valid float value for the label."), 400


    # Define the base folder path for saving data
    base_folder_path = r'C:\Users\JoshuaPaterson\Downloads\Testing3'  # Use raw string

    # Create a new folder with a timestamp or unique identifier
    #timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    new_folder_path = os.path.join(base_folder_path, f'data_{timestamp}')

    # Create the new folder
    os.makedirs(new_folder_path, exist_ok=True)

    # Define the path for the JSON file
    json_file_path = os.path.join(new_folder_path, 'data.json')
    globalErrorVar.NN_Data_Collection_File_path = new_folder_path
    
    # Call the measurement state function
    try:
        measurement_manager.measurement_state_MV3()
    except ValueError:
        return jsonify(message="ERROR with VNA"), 400
    
    if globalErrorVar.ErrorFromMeasurementManager:
        globalErrorVar.ErrorFromMeasurementManager = False
        return jsonify(message="ERROR with VNA"), 400

    # Prepare data to save
    data_to_save = {
        'label': float_value,
        'shearVain20cm': shear_vain_20cm,
        'shearVain50cm': shear_vain_50cm,
        'shearVain80cm': shear_vain_80cm,
        'surfaceLabel': surface_label,
        'heightLabel': height_Label
    }
    
    # Write the input values to a JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(data_to_save, json_file)

    # Define the path to the VNA touchstones directory
    vna_touchstones_dir = r'C:\Users\JoshuaPaterson\Downloads\Testing1\vnaTouchstones'
    latest_folder_path = None
    latest_time = 0

    # Find the latest folder in the vnaTouchstones directory
    for folder in os.listdir(vna_touchstones_dir):
        folder_path = os.path.join(vna_touchstones_dir, folder)
        if os.path.isdir(folder_path):
            folder_time = os.path.getmtime(folder_path)
            if folder_time > latest_time:
                latest_time = folder_time
                latest_folder_path = folder_path

    if latest_folder_path is None:
        return jsonify(message="No folders found in the vnaTouchstones directory."), 400

    # Path to the calibration data folder
    calibration_data_folder = os.path.join(latest_folder_path, 'calData')

    # Check for the existence of the calData folder
    if not os.path.exists(calibration_data_folder):
        return jsonify(message="Calibration data folder does not exist."), 400

    # Construct the S1P file path for the actuator position "210"
    s1p_file_path = os.path.join(calibration_data_folder, '210.s1p')

    # Check if the S1P file exists
    if not os.path.exists(s1p_file_path):
        return jsonify(message="S1P file for actuator position '210' not found."), 400

    # Define the new location for the copied S1P file in the new folder
    new_s1p_file_path = os.path.join(new_folder_path, 'Cal_data.s1p')

    # Copy the S1P file to the new location
    shutil.copy(s1p_file_path, new_s1p_file_path)

    return jsonify(message=f"Data saved to {new_folder_path}")




    
 