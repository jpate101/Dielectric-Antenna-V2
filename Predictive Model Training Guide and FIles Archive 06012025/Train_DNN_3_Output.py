import numpy as np
import os
import json
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint

def read_s_param_file(file_path):
    """Read S-parameter file and return frequencies, S11 components, magnitudes, and phases."""
    frequencies, s11_real, s11_imag = [], [], []
    
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith(('!', '#')):
                continue
            parts = line.split()
            if len(parts) >= 3:
                frequencies.append(float(parts[0]))
                s11_real.append(float(parts[1]))
                s11_imag.append(float(parts[2]))

    frequencies = np.array(frequencies)
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

                    # Extract the shearVain labels
                    shear_vain_20cm = json_data.get('shearVain20cm')
                    shear_vain_50cm = json_data.get('shearVain50cm')
                    shear_vain_80cm = json_data.get('shearVain80cm')

                    # Skip this sample if any of the labels are missing
                    if not (shear_vain_20cm and shear_vain_50cm and shear_vain_80cm):
                        print(f"Skipping sample from '{sample_folder}' due to missing labels.")
                        continue

                    label = [float(shear_vain_20cm), float(shear_vain_50cm), float(shear_vain_80cm)]
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

# Define main folder where data is stored
main_folder = r'C:\Users\JoshuaPaterson\Phibion Pty Ltd\IG88 - General\03 Development\Dielectric Antenna\Predictive Model Training Guide and FIles\Data Labeling Scripts\MT_WELD_OUTPUT'

# Specify if calibration data should be used
use_cal_data = False  # Change to True if calibration data is required
data, labels = load_data_from_folders(main_folder, use_cal_data)

# Check how many valid samples were loaded
print(f"Loaded {len(data)} valid samples.")

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

# Normalize the data
mean_X_train = np.mean(X_train, axis=0)
std_X_train = np.std(X_train, axis=0)
std_X_train[std_X_train == 0] = 1  # Avoid division by zero
X_train = (X_train - mean_X_train) / std_X_train
X_test = (X_test - mean_X_train) / std_X_train

# Reshape the input data for LSTM
X_train_reshaped = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
X_test_reshaped = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))

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
    Dense(3, activation='linear')  # Output layer for 3 values
])

# Compile the model
model.compile(optimizer='rmsprop', loss='mean_squared_error', metrics=['mean_absolute_error'])

# Add model checkpointing
checkpoint = ModelCheckpoint('3_Output_DNN_Model_Best_Validations.keras', save_best_only=True, monitor='val_loss', mode='min')

# Train the model and capture history
history = model.fit(X_train_reshaped, y_train, epochs=120, batch_size=16, validation_split=0.1, callbacks=[checkpoint])

# Evaluate the model
loss, mae = model.evaluate(X_test_reshaped, y_test)

# Combine training and test data for overall evaluation
X_all = np.concatenate((X_train_reshaped, X_test_reshaped), axis=0)
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
model.save('3_Output_DNN_Model_Final.keras')
print("Model saved as 'DNN_Model_Final.keras'")