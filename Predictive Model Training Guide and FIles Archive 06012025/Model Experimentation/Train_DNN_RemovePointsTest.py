import numpy as np
import os
import json
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint
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


def load_data_from_folders(main_folder, use_cal_data):
    """Load data from specified main folder and return combined data and labels."""
    data, labels, latitudes, longitudes = [], [], [], []
    
    for sample_folder in os.listdir(main_folder):
        sample_path = os.path.join(main_folder, sample_folder)
        
        if os.path.isdir(sample_path):
            json_file_path = os.path.join(sample_path, 'data.json')
            s1p_file_paths = [os.path.join(sample_path, f) for f in os.listdir(sample_path) if f.endswith('.s1p')]
            
            # Read the label from the JSON file
            if os.path.exists(json_file_path):
                with open(json_file_path, 'r') as json_file:
                    json_data = json.load(json_file)
                    label = json_data.get('shearVain50cm', None)
                    latitude = json_data.get('latitude', None)
                    longitude = json_data.get('longitude', None)
                    
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
                    
                    # Skip this sample if lat/long is invalid
                    if latitude is None or longitude is None:
                        print(f"Warning: Missing latitude or longitude in '{json_file_path}'. Skipping sample.")
                        continue
                    
                    latitudes.append(float(latitude))
                    longitudes.append(float(longitude))
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

    return np.array(data, dtype=float), np.array(labels), np.array(latitudes), np.array(longitudes)


# Define the list of corrupted points (latitude, longitude)
corrupted_points = [
    (-28.862358, 122.526213),#here 
    (-28.862136, 122.526294),#here 
    (-28.862185, 122.525361),#here 
    (-28.861789, 122.527567),#here 
    (-28.862678, 122.52546)

]


def is_corrupted_point(lat, lon, corrupted_points):
    """Check if the given latitude and longitude match any corrupted points."""
    return (lat, lon) in corrupted_points


# Example usage
main_folder = r'C:\Users\JoshuaPaterson\Phibion Pty Ltd\IG88 - General\03 Development\Dielectric Antenna\Predictive Model Training Guide and FIles\Data Labeling Scripts\MT_WELD_OUTPUT'
use_cal_data = False  # Change this to True if you want to use calibration data

# Load data and labels
data, labels, latitudes, longitudes = load_data_from_folders(main_folder, use_cal_data)

print(f"Loaded {len(data)} samples.")  # Print the number of samples loaded

# Remove samples with corrupted locations
filtered_data = []
filtered_labels = []
filtered_latitudes = []
filtered_longitudes = []

for sample, label, lat, lon in zip(data, labels, latitudes, longitudes):
    if label is not None and not is_corrupted_point(lat, lon, corrupted_points):  # Exclude corrupted points
        filtered_data.append(sample)
        filtered_labels.append(label)
        filtered_latitudes.append(lat)
        filtered_longitudes.append(lon)

# Convert filtered data and labels to numpy arrays
X_filtered = np.array(filtered_data, dtype=float)
y_filtered = np.array(filtered_labels, dtype=float)

# Handle varying lengths by padding
max_length = max(len(sample) for sample in X_filtered)  # Find the max length

# Pad samples to ensure uniformity
X_padded = np.array([np.pad(sample, (0, max_length - len(sample)), 'constant') for sample in X_filtered], dtype=float)

# Reshape the input data for LSTM
X_train_reshaped = X_padded.reshape((X_padded.shape[0], 1, X_padded.shape[1]))

# Check for NaN values in X_train_reshaped and y_filtered
print("NaN values in X_train_reshaped:", np.any(np.isnan(X_train_reshaped)))
print("NaN values in y_filtered:", np.any(np.isnan(y_filtered)))

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_train_reshaped, y_filtered, test_size=0.1)

# Build the neural network for regression
model = Sequential([
    LSTM(724, input_shape=(X_train_reshaped.shape[1], X_train_reshaped.shape[2]), return_sequences=True),
    Dropout(0.05),
    LSTM(512),
    Dropout(0.05),
    Dense(262, activation='relu'),
    Dense(128, activation='relu'),
    Dense(64, activation='relu'),
    Dense(32, activation='relu'),
    Dense(16, activation='relu'),
    Dense(1, activation='linear')
])

# Compile the model
model.compile(optimizer='rmsprop', loss='mean_squared_error', metrics=['mean_absolute_error'])

# Add model checkpointing
checkpoint = ModelCheckpoint('50_DNN_MT_WELD_RemovePointsTestingCheck.keras', save_best_only=True, monitor='val_loss', mode='min')

# Train the model and capture history
history = model.fit(X_train, y_train, epochs=120, batch_size=16, validation_split=0.2, callbacks=[checkpoint])

# Evaluate the model
loss, mae = model.evaluate(X_test, y_test)

# Combine training and test data for overall evaluation
X_all = np.concatenate((X_train, X_test), axis=0)
y_all = np.concatenate((y_train, y_test), axis=0)
loss_all, mae_all = model.evaluate(X_all, y_all)
print(f'Test Mean Absolute Error: {mae:.2f}')
print(f'Overall Mean Absolute Error on All Data: {mae_all:.2f}')

# Plot training & validation loss values
plt.figure(figsize=(10, 5))
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(loc='upper right')
plt.show()

# Save the model
model.save('50_DNN_MT_WELD_RemovePointsTestingCheck.keras')
print("Model saved as '50_DNN_MT_WELD_RemovePointsTestingCheck.keras'")
