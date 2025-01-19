import numpy as np
import os
import json
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.metrics import mean_absolute_error
from datetime import datetime

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
                    shear_vain_20cm = json_data.get('shearVain20cm', None)
                    shear_vain_50cm = json_data.get('shearVain50cm', None)
                    shear_vain_80cm = json_data.get('shearVain80cm', None)
                    timestamp = json_data.get('timestamp', str(datetime.now()))  # Use current time if not present
                    if all([shear_vain_20cm, shear_vain_50cm, shear_vain_80cm]):
                        try:
                            label = [float(shear_vain_20cm), float(shear_vain_50cm), float(shear_vain_80cm)]
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
lstm_model = load_model('3_Output_DNN_Model_Best_Validations.keras')

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

# Calculate the Mean Absolute Error (MAE) for each output
mae_output_1 = mean_absolute_error(y_filtered[:, 0], y_pred_lstm[:, 0])
mae_output_2 = mean_absolute_error(y_filtered[:, 1], y_pred_lstm[:, 1])
mae_output_3 = mean_absolute_error(y_filtered[:, 2], y_pred_lstm[:, 2])

# Print the MAE for each output
print(f"Mean Absolute Error for Output 1 (Shear Vain 20cm): {mae_output_1:.4f}")
print(f"Mean Absolute Error for Output 2 (Shear Vain 50cm): {mae_output_2:.4f}")
print(f"Mean Absolute Error for Output 3 (Shear Vain 80cm): {mae_output_3:.4f}")

# Calculate the maximum error (worst error) for each output
errors_output_1 = np.abs(y_filtered[:, 0] - y_pred_lstm[:, 0])
errors_output_2 = np.abs(y_filtered[:, 1] - y_pred_lstm[:, 1])
errors_output_3 = np.abs(y_filtered[:, 2] - y_pred_lstm[:, 2])

max_error_output_1 = np.max(errors_output_1)
max_error_output_2 = np.max(errors_output_2)
max_error_output_3 = np.max(errors_output_3)

print(f"Maximum Error for Output 1: {max_error_output_1:.4f}")
print(f"Maximum Error for Output 2: {max_error_output_2:.4f}")
print(f"Maximum Error for Output 3: {max_error_output_3:.4f}")

# Create a pandas DataFrame to display the labels vs predicted values for LSTM model
df = pd.DataFrame({
    'Sample Index': np.arange(1, len(y_filtered) + 1),
    'True Label 20cm': y_filtered[:, 0],
    'Predicted 20cm (LSTM)': y_pred_lstm[:, 0],
    'Error 20cm (LSTM)': errors_output_1,
    'True Label 50cm': y_filtered[:, 1],
    'Predicted 50cm (LSTM)': y_pred_lstm[:, 1],
    'Error 50cm (LSTM)': errors_output_2,
    'True Label 80cm': y_filtered[:, 2],
    'Predicted 80cm (LSTM)': y_pred_lstm[:, 2],
    'Error 80cm (LSTM)': errors_output_3,
    'Timestamp': filtered_timestamps  # Add the timestamp column
})

# Print the table showing each sample's label vs predicted value for LSTM model
print("\nSample Label vs Predicted Value (LSTM):")
print(df)

# Optionally, save the table to a CSV file
df.to_csv('prediction_comparison_LSTM.csv', index=False)
print("\nThe comparison table has been saved to 'prediction_comparison_LSTM.csv'.")