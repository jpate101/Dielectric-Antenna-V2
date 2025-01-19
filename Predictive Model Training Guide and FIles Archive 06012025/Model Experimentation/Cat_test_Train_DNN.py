import numpy as np
import os
import json
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical


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
                    label = json_data.get('shearVain50cm', None)
                    
                    # Attempt to convert the label to an integer (or float if necessary)
                    if label is not None:
                        try:
                            label = float(label)  # Convert to float (since it's in range 0-120, it can be a float)
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

# Function to categorize labels into 5 categories
def categorize_labels(labels):
    categories = []
    for label in labels:
        if label is None:
            categories.append(None)
        elif label < 0:
            categories.append(0)
        elif label <= 24:
            categories.append(0)
        elif label <= 49:
            categories.append(1)
        elif label <= 74:
            categories.append(2)
        elif label <= 99:
            categories.append(3)
        elif label <= 120:
            categories.append(4)
        else:
            categories.append(4)
    return np.array(categories)

# Example usage
main_folder = r'C:\Users\JoshuaPaterson\Phibion Pty Ltd\IG88 - General\03 Development\Dielectric Antenna\Predictive Model Training Guide and FIles\Data Labeling Scripts\MT_WELD_OUTPUT'
use_cal_data = False  # Change this to True if you want to use calibration data
data, labels = load_data_from_folders(main_folder, use_cal_data)

print(f"Loaded {len(data)} samples.")  # Print the number of samples loaded

# Remove samples where the label is None
filtered_data = []
filtered_labels = []

for sample, label in zip(data, labels):
    if label is not None:  # Only include samples with a valid label
        filtered_data.append(sample)
        filtered_labels.append(label)

# Convert filtered data and labels to numpy arrays
X_filtered = np.array(filtered_data, dtype=float)
y_filtered = np.array(filtered_labels, dtype=float)

# Categorize the labels into 5 categories
y_categorized = categorize_labels(y_filtered)

# One-hot encode the labels for classification
y_categorized_one_hot = to_categorical(y_categorized, num_classes=5)

# Handle varying lengths by padding
max_length = max(len(sample) for sample in X_filtered)  # Find the max length

# Pad samples to ensure uniformity
X_padded = np.array([np.pad(sample, (0, max_length - len(sample)), 'constant') for sample in X_filtered], dtype=float)

# Reshape the input data for LSTM
X_train_reshaped = X_padded.reshape((X_padded.shape[0], 1, X_padded.shape[1]))

# Check for NaN values in X_train_reshaped and y_filtered
print("NaN values in X_train_reshaped:", np.any(np.isnan(X_train_reshaped)))
print("NaN values in y_filtered:", np.any(np.isnan(y_categorized_one_hot)))

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_train_reshaped, y_categorized_one_hot, test_size=0.1)

# Build the neural network for classification
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
    Dense(5, activation='softmax')  # 5 categories for classification
])

# Compile the model
model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

# Add model checkpointing
checkpoint = ModelCheckpoint('50_DNN_MT_WELD_Testing_classificationCheck.keras', save_best_only=True, monitor='val_loss', mode='min')

# Train the model and capture history
history = model.fit(X_train, y_train, epochs=120, batch_size=16, validation_split=0.1, callbacks=[checkpoint])

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)

# Combine training and test data for overall evaluation
X_all = np.concatenate((X_train, X_test), axis=0)
y_all = np.concatenate((y_train, y_test), axis=0)
loss_all, accuracy_all = model.evaluate(X_all, y_all)
print(f'Test Accuracy: {accuracy:.2f}')
print(f'Overall Accuracy on All Data: {accuracy_all:.2f}')

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
model.save('50_DNN_MT_WELD_Testing_classification.keras')
print("Model saved as '50_DNN_MT_WELD_Testing_classification.keras'")