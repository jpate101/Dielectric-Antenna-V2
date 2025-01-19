import numpy as np
import os
import json
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import joblib  # For saving the model

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
    """Load data from specified main folder and return combined data."""
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

# Example usage
main_folder = r'C:\Users\JoshuaPaterson\Phibion Pty Ltd\IG88 - General\03 Development\Dielectric Antenna\Predictive Model Training Guide and FIles\Data Labeling Scripts\MT_WELD_OUTPUT'
use_cal_data = False  # Change this to True if you want to use calibration data

# Load the data and labels
data, labels = load_data_from_folders(main_folder, use_cal_data)

# Remove samples where the label is None
filtered_data = []

for sample in data:
    filtered_data.append(sample)

# Convert filtered data to numpy array
X_filtered = np.array(filtered_data, dtype=float)

# Ensure the data is a valid numpy array of float type
if not np.issubdtype(X_filtered.dtype, np.floating):
    print("Converting data to float type.")
    X_filtered = X_filtered.astype(float)

# Check the shape of the data before scaling
print(f"Shape of X_filtered before scaling: {X_filtered.shape}")
if X_filtered.ndim == 1:
    print("Warning: Data is 1D, reshaping to 2D")
    X_filtered = X_filtered.reshape(-1, 1)  # Reshaping to 2D if necessary

# Standardize the data (important for KMeans)
scaler = StandardScaler()

# Verify the data is a valid 2D array
if X_filtered.shape[0] > 0 and X_filtered.shape[1] > 0:
    X_scaled = scaler.fit_transform(X_filtered)
else:
    raise ValueError("Filtered data is empty or incorrectly shaped!")

# Manually set the value of k (number of clusters)
k = 2  # You can change this value based on your preference

# Perform K-Means clustering with the manually selected k
kmeans = KMeans(n_clusters=k)
y_kmeans = kmeans.fit_predict(X_scaled)

# Print the cluster centers
print(f"Cluster Centers:\n{kmeans.cluster_centers_}")

# Save the KMeans model using joblib
joblib.dump(kmeans, 'kmeans_model.pkl')
print("KMeans model saved as 'kmeans_model.pkl'.")

# Save the cluster labels (optional)
np.save('cluster_labels.npy', y_kmeans)
print("Cluster labels saved as 'cluster_labels.npy'.")

# Plotting the clusters using PCA for 2D visualization
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Plot the data points colored by the predicted cluster labels
plt.figure(figsize=(8, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y_kmeans, cmap='viridis', marker='o')
plt.title(f'Clusters Visualization using PCA (k={k})')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.colorbar(label='Cluster Label')
plt.show()