import os
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

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

def preprocess_s1p_data(folder_path, gps_dict):
    """Preprocess the S1P files in a folder for predictions and extract coordinates from gps_dict."""
    data = []
    coordinates = []
    
    # Debugging: Print the contents of the folder
    print(f"Processing folder: {folder_path}")
    
    # List files in the folder and filter for .s1p files
    s1p_file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.s1p')]
    
    if not s1p_file_paths:
        print(f"Warning: No .s1p files found in '{folder_path}'")
    
    for file in s1p_file_paths:
        print(f"Processing file: {file}")  # Debug: print file path
        
        # Extract filename without extension for matching with GPS data
        file_name_without_extension = os.path.splitext(os.path.basename(file))[0]
        
        # Check if the file has a corresponding GPS entry
        if file_name_without_extension not in gps_dict:
            print(f"Warning: No matching GPS data found for {file_name_without_extension}. Skipping this file.")
            continue
        
        # Get GPS coordinates from the dictionary
        latitude, longitude = gps_dict[file_name_without_extension]
        
        s11_real, s11_imag, magnitudes, phases = read_s_param_file(file)
        sample_data = np.concatenate([s11_real, s11_imag, magnitudes, phases])
        data.append(sample_data)
        coordinates.append((latitude, longitude))
    
    return np.array(data), np.array(coordinates)

# Load the trained model
model = load_model('50_DNN_MT_WELD_Testing_classification.keras')

# Paths to the S1P folders (Day 1 and Day 2)
day1_folder = r'C:\Users\JoshuaPaterson\Phibion Pty Ltd\IG88 - General\03 Development\Dielectric Antenna\Predictive Model Training Guide and FIles\Data Labeling Scripts\Mt Weld S1P - Day 1\S1P Merge'
day2_folder = r'C:\Users\JoshuaPaterson\Phibion Pty Ltd\IG88 - General\03 Development\Dielectric Antenna\Predictive Model Training Guide and FIles\Data Labeling Scripts\Mt Weld S1P - Day 2\S1P Merge'

# Load GPS data from CSV files (replace with actual paths to your GPS data)
gps_data_day1_file = r'C:\Users\JoshuaPaterson\Phibion Pty Ltd\IG88 - General\03 Development\Dielectric Antenna\Predictive Model Training Guide and FIles\Data Labeling Scripts\Mt Weld S1P - Day 1\CSV_D1_Merge.csv'
gps_data_day2_file = r'C:\Users\JoshuaPaterson\Phibion Pty Ltd\IG88 - General\03 Development\Dielectric Antenna\Predictive Model Training Guide and FIles\Data Labeling Scripts\Mt Weld S1P - Day 2\CSV_D2_Merge.csv'

# Load Day 1 and Day 2 GPS data from CSV files
gps_data_day1_df = pd.read_csv(gps_data_day1_file)
gps_data_day2_df = pd.read_csv(gps_data_day2_file)

# Create dictionaries to map vna_filename (without .s1p extension) to the corresponding GPS data for Day 1 and Day 2
gps_dict_day1 = {os.path.splitext(row['vna_filename'])[0]: (row['latitude'], row['longitude']) for _, row in gps_data_day1_df.iterrows()}
gps_dict_day2 = {os.path.splitext(row['vna_filename'])[0]: (row['latitude'], row['longitude']) for _, row in gps_data_day2_df.iterrows()}

# Preprocess data for Day 1 and Day 2 using their respective GPS dictionaries
data_day1, coordinates_day1 = preprocess_s1p_data(day1_folder, gps_dict_day1)
data_day2, coordinates_day2 = preprocess_s1p_data(day2_folder, gps_dict_day2)

# Combine data from both days
data_combined = np.concatenate((data_day1, data_day2), axis=0)
coordinates_combined = np.concatenate((coordinates_day1, coordinates_day2), axis=0)

# Debugging: Check the data_combined length
print(f"Total samples processed: {len(data_combined)}")

# Ensure that there is data to process
if len(data_combined) == 0:
    raise ValueError("No valid data found for prediction. Please check the S1P files and folder paths.")

# Pad data to ensure uniformity (same length for LSTM)
max_length = max(len(sample) for sample in data_combined)  # Find the max length
X_padded = np.array([np.pad(sample, (0, max_length - len(sample)), 'constant') for sample in data_combined], dtype=float)

# Reshape for LSTM model
X_padded_reshaped = X_padded.reshape((X_padded.shape[0], 1, X_padded.shape[1]))

# Predict the categories
predictions = model.predict(X_padded_reshaped)

# Convert predictions from one-hot to category index
predicted_classes = np.argmax(predictions, axis=1)

# Convert predicted classes to integer labels (e.g., 0 for 0-24, 1 for 25-49, etc.)
predicted_labels = [0 if class_idx == 0 else 1 if class_idx == 1 else 2 if class_idx == 2 else 3 if class_idx == 3 else 4 for class_idx in predicted_classes]

# Create a DataFrame to store latitude, longitude, and predicted category
output_data = {
    'latitude': [coord[0] for coord in coordinates_combined],
    'longitude': [coord[1] for coord in coordinates_combined],
    'predicted_category': predicted_labels
}

df = pd.DataFrame(output_data)

# Save to CSV
output_csv_path = 'cat_s1p_predictions_only.csv'
df.to_csv(output_csv_path, index=False)

print(f"Predictions saved to {output_csv_path}")