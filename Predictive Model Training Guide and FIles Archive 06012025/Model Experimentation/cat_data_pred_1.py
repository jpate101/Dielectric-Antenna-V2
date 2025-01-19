import os
import json
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.metrics import accuracy_score


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


def preprocess_data(main_folder, use_cal_data=False):
    """Preprocess data and prepare for predictions."""
    data = []
    coordinates = []
    real_labels = []
    
    for sample_folder in os.listdir(main_folder):
        sample_path = os.path.join(main_folder, sample_folder)
        
        if os.path.isdir(sample_path):
            json_file_path = os.path.join(sample_path, 'data.json')
            s1p_file_paths = [os.path.join(sample_path, f) for f in os.listdir(sample_path) if f.endswith('.s1p')]
            
            # Read the label from the JSON file
            if os.path.exists(json_file_path):
                with open(json_file_path, 'r') as json_file:
                    json_data = json.load(json_file)
                    latitude = json_data.get('latitude', None)
                    longitude = json_data.get('longitude', None)
                    
                    # Skip the sample if latitude or longitude is not available
                    if latitude is None or longitude is None:
                        continue
                    
                    coordinates.append((latitude, longitude))
                    
                    # Get the real label (shearVain50cm)
                    shearVain50cm = json_data.get('shearVain50cm', None)
                    if shearVain50cm is not None:
                        real_labels.append(float(shearVain50cm))
                    else:
                        real_labels.append(None)  # If real label is missing, append None
                    
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
                                
                        data.append(sample_data)
                    else:
                        print(f"Warning: No valid .s1p file found in '{sample_path}'.")
            else:
                print(f"Warning: '{json_file_path}' not found.")
    
    return np.array(data), np.array(coordinates), np.array(real_labels)


# Load the trained model
model = load_model('50_DNN_MT_WELD_Testing_classification.keras')

# Preprocess the data
main_folder = r'C:\Users\JoshuaPaterson\Phibion Pty Ltd\IG88 - General\03 Development\Dielectric Antenna\Predictive Model Training Guide and FIles\Data Labeling Scripts\MT_WELD_OUTPUT'
data, coordinates, real_labels = preprocess_data(main_folder, use_cal_data=False)

# Pad data to ensure uniformity (same length for LSTM)
max_length = max(len(sample) for sample in data)  # Find the max length
X_padded = np.array([np.pad(sample, (0, max_length - len(sample)), 'constant') for sample in data], dtype=float)

# Reshape for LSTM model
X_padded_reshaped = X_padded.reshape((X_padded.shape[0], 1, X_padded.shape[1]))

# Predict the categories
predictions = model.predict(X_padded_reshaped)

# Convert predictions from one-hot to category index
predicted_classes = np.argmax(predictions, axis=1)

# Convert predicted classes to integer labels (e.g., 0 for 0-24, 1 for 25-49, etc.)
predicted_labels = [0 if class_idx == 0 else 1 if class_idx == 1 else 2 if class_idx == 2 else 3 if class_idx == 3 else 4 for class_idx in predicted_classes]

# Map the real label values to integer labels
def map_to_integer_label(real_value):
    if real_value <= 24:
        return 0
    elif real_value <= 49:
        return 1
    elif real_value <= 74:
        return 2
    elif real_value <= 99:
        return 3
    else:
        return 4

real_labels_integer = [map_to_integer_label(value) if value is not None else None for value in real_labels]

# Calculate accuracy
valid_indices = [i for i, label in enumerate(real_labels_integer) if label is not None]  # Ignore samples with missing real labels
valid_predicted_labels = [predicted_labels[i] for i in valid_indices]
valid_real_labels = [real_labels_integer[i] for i in valid_indices]

accuracy = accuracy_score(valid_real_labels, valid_predicted_labels)
print(f"Accuracy: {accuracy * 100:.2f}%")

# Create a DataFrame to store latitude, longitude, predicted category, and real label category
output_data = {
    'latitude': [coord[0] for coord in coordinates],
    'longitude': [coord[1] for coord in coordinates],
    'predicted_category': predicted_labels,
    'real_label_category': real_labels_integer
}

df = pd.DataFrame(output_data)

# Save to CSV
output_csv_path = 'cat_predictions_with_real_labels.csv'
df.to_csv(output_csv_path, index=False)

print(f"Predictions and real labels saved to {output_csv_path}")