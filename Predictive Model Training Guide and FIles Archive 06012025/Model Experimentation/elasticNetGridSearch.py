# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 12:23:25 2025

@author: JoshuaPaterson
"""

import numpy as np
import os
import joblib  # For saving the model
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import StandardScaler
import json
from sklearn.model_selection import GridSearchCV

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

def load_data_from_folders(main_folder, use_cal_data):
    """Load data from specified main folder and return combined data and labels."""
    data, labels = [], []
    
    for sample_folder in os.listdir(main_folder):
        sample_path = os.path.join(main_folder, sample_folder)
        
        if os.path.isdir(sample_path):
            json_file_path = os.path.join(sample_path, 'data.json')
            s1p_file_paths = [os.path.join(sample_path, f) for f in os.listdir(sample_path) if f.endswith('.s1p')]
            
            # Read the label from the JSON file
            if os.path.exists(json_file_path):
                with open(json_file_path, 'r') as json_file:
                    json_data = json.load(json_file)
                    label = json_data.get('shearVain80cm', None)
                    
                    # Attempt to convert the label to an integer (or float if necessary)
                    if label is not None:
                        try:
                            label = int(label)  # Try to convert to an integer
                        except ValueError:
                            try:
                                label = float(label)  # Try to convert to a float if it's not an int
                            except ValueError:
                                print(f"Warning: Unable to convert label '{label}' to a number.")
                                label = None  # Set to None if conversion fails
                    
                    labels.append(label)
            else:
                print(f"Warning: '{json_file_path}' not found.")

            # Read the first valid S-parameter file
            if s1p_file_paths:
                s11_real, s11_imag, magnitudes, phases = read_s_param_file(s1p_file_paths[0])
                sample_data = np.concatenate([s11_real, s11_imag, magnitudes, phases])
                
                if use_cal_data:
                    # Check for calibration data
                    cal_file_path = os.path.join(sample_path, 'Cal_data.s1p')
                    if os.path.exists(cal_file_path):
                        cal_real, cal_imag, cal_magnitudes, cal_phases = read_s_param_file(cal_file_path)
                        cal_data = np.concatenate([cal_real, cal_imag, cal_magnitudes, cal_phases])
                        sample_data = np.concatenate([sample_data, cal_data])
                    else:
                        print(f"Warning: Calibration data not found in '{sample_path}'. Using sample data without calibration.")

                data.append(sample_data)
                print(f"Loaded sample data with shape: {sample_data.shape}")  # Debugging output
            else:
                print(f"Warning: No valid .s1p file found in '{sample_path}'.")

    return np.array(data, dtype=float), np.array(labels)

# Example usage
main_folder = r'C:\Users\JoshuaPaterson\Phibion Pty Ltd\IG88 - General\03 Development\Dielectric Antenna\Predictive Model Training\Data Processing Scripts\MT_WELD_OUTPUT'
use_cal_data = False  # Set to True if you want to include calibration data

# Load data
data, labels = load_data_from_folders(main_folder, use_cal_data)

# Check the loaded data shape
print(f"Loaded {len(data)} samples.")
print(f"Shape of data: {data.shape}")
print(f"Shape of labels: {labels.shape}")

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2)


# Normalize the data using StandardScaler
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Define the model
elasticnet_model = ElasticNet(max_iter=5000)

# Define the hyperparameter grid
param_grid = {
    'alpha': [0.1, 0.5, 1.0, 2.0, 10.0],  # Regularization strength
    'l1_ratio': [0.1, 0.5, 0.7, 0.9],    # Mix between Lasso (L1) and Ridge (L2)
}

# Set up GridSearchCV with cross-validation (CV=5 means 5-fold cross-validation)
grid_search = GridSearchCV(estimator=elasticnet_model, param_grid=param_grid, 
                           scoring='neg_mean_absolute_error', cv=2, n_jobs=1, verbose=1)

# Fit the grid search to the training data
grid_search.fit(X_train, y_train)

# Print the best parameters found
print("Best Hyperparameters found by GridSearchCV:")
print(grid_search.best_params_)

# Get the best model with the found parameters
best_model = grid_search.best_estimator_

# Make predictions with the best model
y_pred_train = best_model.predict(X_train)
y_pred_test = best_model.predict(X_test)

# Evaluate the model
train_mae = mean_absolute_error(y_train, y_pred_train)
test_mae = mean_absolute_error(y_test, y_pred_test)

print(f"Training Mean Absolute Error: {train_mae:.2f}")
print(f"Test Mean Absolute Error: {test_mae:.2f}")

# Save the trained model and scaler
joblib.dump(best_model, 'best_elasticnet_model.pkl')
joblib.dump(scaler, 'best_scaler.pkl')
print("Best model and scaler saved as 'best_elasticnet_model.pkl' and 'best_scaler.pkl'")

print("GridSearchCV complete!")