# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 07:49:44 2024

@author: JoshuaPaterson
"""

import numpy as np
import os
import json
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.metrics import mean_absolute_error
from datetime import datetime
import joblib

def read_s_param_file(file_path):
    """Read S-parameter file and return magnitudes, phases, real, and imaginary components."""
    s11_real, s11_imag = [], []
    
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith(('!', '#')):  # Skip comments
                continue
            parts = line.split()
            if len(parts) >= 3:
                s11_real.append(float(parts[1]))
                s11_imag.append(float(parts[2]))

    s11_real = np.array(s11_real)
    s11_imag = np.array(s11_imag)
    
    magnitudes = np.sqrt(s11_real**2 + s11_imag**2)
    phases = np.arctan2(s11_imag, s11_real)

    return s11_real, s11_imag, magnitudes, phases

def prepare_data_for_model(X):
    """Prepare the data for LSTM by padding and reshaping."""
    max_length = max(len(sample) for sample in X)  # Find the max length
    X_padded = np.array([np.pad(sample, (0, max_length - len(sample)), 'constant') for sample in X], dtype=float)
    return X_padded.reshape((X_padded.shape[0], 1, X_padded.shape[1]))

# Load the trained LSTM model
lstm_model = load_model('50_DNN_MT_WELD_Testing_D2OnlyCheck.keras')

# Load the ElasticNet model and scaler
elasticnet_model = joblib.load('50_EN_MT_WELD.pkl')
scaler = joblib.load('50_EN_MT_WELD_scaler.pkl')

# Load the GPS data from the CSV
gps_data_file = r'C:\Users\JoshuaPaterson\OneDrive - Phibion Pty Ltd\Documents\GitHub\Dielectric-Antenna-V2\Predictive Model Training Guide and FIles Archive 06012025\MT Weld Raw Data\Mt Weld S1P - Day 1\CSV_D1_Merge.csv'  # Provide the correct path to your GPS CSV file
gps_data_df = pd.read_csv(gps_data_file)

# Create a dictionary to map vna_filename to the corresponding GPS data
gps_dict = {row['vna_filename']: (row['latitude'], row['longitude']) for _, row in gps_data_df.iterrows()}
#print(gps_dict)

# Folder containing the S1P files
s1p_folder = r'C:\Users\JoshuaPaterson\OneDrive - Phibion Pty Ltd\Documents\GitHub\Dielectric-Antenna-V2\Predictive Model Training Guide and FIles Archive 06012025\MT Weld Raw Data\Mt Weld S1P - Day 1\S1P Merge'

# List to hold the final results
results = []

# Process each S1P file in the folder
for filename in os.listdir(s1p_folder):
    if filename.endswith('.s1p'):
        # Extract the name (without extension) to correlate with GPS data
        file_name_without_extension = os.path.splitext(filename)[0]
        
        # Add the .s1p extension to file_name_without_extension to match the GPS dictionary keys
        full_filename = file_name_without_extension + '.s1p'
        
        # Check if the full filename (with .s1p) exists in the GPS data dictionary
        if full_filename in gps_dict:
            latitude, longitude = gps_dict[full_filename]
            
            # Full path of the current S1P file
            file_path = os.path.join(s1p_folder, filename)
            
            # Read the S-parameter data
            s11_real, s11_imag, magnitudes, phases = read_s_param_file(file_path)
            sample_data = np.concatenate([s11_real, s11_imag, magnitudes, phases])
            
            # Prepare the data for the LSTM model
            X_reshaped = prepare_data_for_model([sample_data])
            
            # Use the LSTM model to predict
            y_pred_lstm = lstm_model.predict(X_reshaped).flatten()
            
            # Use the ElasticNet model to predict
            X_scaled = scaler.transform([sample_data])  # Scale the data using the same scaler
            y_pred_en = elasticnet_model.predict(X_scaled)
            
            
            # Store results
            results.append({
                'Filename': filename,
                'Latitude': latitude,
                'Longitude': longitude,
                'LSTM Prediction': y_pred_lstm[0],
                'ElasticNet Prediction': y_pred_en[0]
            })

# Convert results into a DataFrame
results_df = pd.DataFrame(results)

# Save results to a CSV file
output_file = r'C:\Users\JoshuaPaterson\OneDrive - Phibion Pty Ltd\Documents\GitHub\Dielectric-Antenna-V2\Predictive Model Training Guide and FIles Archive 06012025\Model Experimentation\D1_Final_MT_WELD_EN.csv'  # Adjust the output file path
results_df.to_csv(output_file, index=False)

print(f"Results have been saved to {output_file}")