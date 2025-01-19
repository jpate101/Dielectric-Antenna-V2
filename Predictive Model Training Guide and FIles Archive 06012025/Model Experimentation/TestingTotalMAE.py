import numpy as np
import os
import json
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.metrics import mean_absolute_error
from datetime import datetime
import joblib  # For loading the ElasticNet model and scaler

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

def load_data_from_folders(main_folder):
    """Load data and labels from the folder containing .s1p and data.json."""
    data, labels, timestamps = [], [], []
    
    for sample_folder in os.listdir(main_folder):
        sample_path = os.path.join(main_folder, sample_folder)
        
        if os.path.isdir(sample_path):
            json_file_path = os.path.join(sample_path, 'data.json')
            s1p_file_paths = [os.path.join(sample_path, f) for f in os.listdir(sample_path) if f.endswith('.s1p')]
            
            # Read the label and timestamp from the JSON file
            if os.path.exists(json_file_path):
                with open(json_file_path, 'r') as json_file:
                    json_data = json.load(json_file)
                    label = json_data.get('shearVain50cm', None)
                    timestamp = json_data.get('timestamp', str(datetime.now()))  # Use current time if not present
                    if label is not None:
                        try:
                            label = float(label)
                        except ValueError:
                            print(f"Warning: Unable to convert label '{label}' to a number.")
                            label = None
                    labels.append(label)
                    timestamps.append(timestamp)  # Add timestamp to the list
            
            # Process the S-parameter data from the first .s1p file
            if s1p_file_paths:
                s11_real, s11_imag, magnitudes, phases = read_s_param_file(s1p_file_paths[0])
                sample_data = np.concatenate([s11_real, s11_imag, magnitudes, phases])
                data.append(sample_data)
    
    return np.array(data, dtype=float), np.array(labels), timestamps

def prepare_data_for_model(X):
    """Prepare the data for LSTM by padding and reshaping."""
    max_length = max(len(sample) for sample in X)  # Find the max length
    X_padded = np.array([np.pad(sample, (0, max_length - len(sample)), 'constant') for sample in X], dtype=float)
    return X_padded.reshape((X_padded.shape[0], 1, X_padded.shape[1]))

# Load the trained LSTM model
lstm_model = load_model('50_DNN_MT_WELD_RemovePointsTestingCheck.keras')

# Load the ElasticNet model and scaler
elasticnet_model = joblib.load('50_EN_MT_WELD_T12.pkl')
scaler = joblib.load('50_EN_MT_WELD_T12_scaler.pkl')

# Load the data from the folders
main_folder = r'C:\Users\JoshuaPaterson\Phibion Pty Ltd\IG88 - General\03 Development\Dielectric Antenna\Predictive Model Training Guide and FIles\Data Labeling Scripts\MT_WELD_OUTPUT'
data, labels, timestamps = load_data_from_folders(main_folder)

# Remove samples where the label is None
filtered_data = []
filtered_labels = []
filtered_timestamps = []

for sample, label, timestamp in zip(data, labels, timestamps):
    if label is not None:  # Only include samples with a valid label
        filtered_data.append(sample)
        filtered_labels.append(label)
        filtered_timestamps.append(timestamp)

# Convert filtered data, labels, and timestamps to numpy arrays
X_filtered = np.array(filtered_data, dtype=float)
y_filtered = np.array(filtered_labels, dtype=float)

# Prepare the data for the LSTM model
X_reshaped = prepare_data_for_model(X_filtered)

# Use the LSTM model to predict on each sample
y_pred_lstm = lstm_model.predict(X_reshaped)
y_pred_lstm = y_pred_lstm.flatten()  # Flatten predictions

# Use the ElasticNet model to predict
X_scaled = scaler.transform(X_filtered)  # Scale the data using the same scaler
y_pred_en = elasticnet_model.predict(X_scaled)

# Calculate the Mean Absolute Error (MAE) for both models
mae_lstm = mean_absolute_error(y_filtered, y_pred_lstm)
mae_en = mean_absolute_error(y_filtered, y_pred_en)

# Calculate the maximum error (worst error) for both models
errors_lstm = np.abs(y_filtered - y_pred_lstm)
errors_en = np.abs(y_filtered - y_pred_en)

max_error_lstm = np.max(errors_lstm)
max_error_en = np.max(errors_en)

# Find the second worst error (second largest error) for both models
sorted_indices_lstm = np.argsort(errors_lstm)[::-1]
second_max_error_lstm = errors_lstm[sorted_indices_lstm[1]]
second_max_error_index_lstm = sorted_indices_lstm[1]

sorted_indices_en = np.argsort(errors_en)[::-1]
second_max_error_en = errors_en[sorted_indices_en[1]]
second_max_error_index_en = sorted_indices_en[1]

# Count the number of samples where the error is greater than 21 for both models
samples_out_of_range_lstm = np.sum(errors_lstm > 16)
samples_out_of_range_en = np.sum(errors_en > 16)

# Output the comparison results
print(f"LSTM Model - Mean Absolute Error (MAE): {mae_lstm:.4f}")
print(f"ElasticNet Model - Mean Absolute Error (MAE): {mae_en:.4f}")
print(f"LSTM Model - Maximum (Worst) Error: {max_error_lstm:.4f}")
print(f"ElasticNet Model - Maximum (Worst) Error: {max_error_en:.4f}")
print(f"Samples with error > 16 for LSTM: {samples_out_of_range_lstm}")
print(f"Samples with error > 16 for ElasticNet: {samples_out_of_range_en}")

# Create a pandas DataFrame to display the labels vs predicted values for both models
df = pd.DataFrame({
    'Sample Index': np.arange(1, len(y_filtered) + 1),
    'True Label': y_filtered,
    'Predicted (LSTM)': y_pred_lstm,
    'Predicted (ElasticNet)': y_pred_en,
    'Error (LSTM)': errors_lstm,
    'Error (ElasticNet)': errors_en,
    'Timestamp': filtered_timestamps  # Add the timestamp column
})

# Print the table showing each sample's label vs predicted value for both models
print("\nSample Label vs Predicted Value (LSTM vs ElasticNet):")
print(df)

# Optionally, save the table to a CSV file
df.to_csv('50_prediction_RemovePointsTest.csv', index=False)
print("\nThe comparison table has been saved to 'prediction_comparison_both_models.csv'.")