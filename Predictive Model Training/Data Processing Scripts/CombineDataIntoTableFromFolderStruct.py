import os
import json
import pandas as pd

# Function to read the S1P data and format it as a block of text
def read_s1p(file_path):
    s1p_data = []
    with open(file_path, 'r') as f:
        # Skip the first three lines of the S1P file (metadata lines)
        for _ in range(3):
            next(f)
        
        # Read the frequency, Re(S11), and Im(S11) values
        for line in f:
            parts = line.split()
            frequency = parts[0]
            re_s11 = parts[1]
            im_s11 = parts[2]
            s1p_data.append(f"{frequency} {re_s11} {im_s11}")
    
    # Join the S1P data into a single string (block of text with line breaks)
    return "\n".join(s1p_data)

# Function to read JSON file and return the metadata
def read_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

# Function to create CSV from folder data
def create_csv(data_folder, output_csv):
    # List to store rows for the CSV
    rows = []
    
    # Counters for stats
    total_samples = 0
    skipped_samples = 0
    skipped_samples_names = []  # List to store the names of skipped samples
    
    # Iterate over all sample folders in the data folder
    for sample_folder in os.listdir(data_folder):
        sample_path = os.path.join(data_folder, sample_folder)
        
        # Check if it is a directory (a sample folder)
        if os.path.isdir(sample_path):
            total_samples += 1
            
            # Define the path for the JSON file
            json_file = os.path.join(sample_path, 'data.json')
            
            # Find the first S1P file in the sample folder (it could have any name ending in .s1p)
            s1p_file = None
            for file in os.listdir(sample_path):
                if file.endswith('.s1p'):
                    s1p_file = os.path.join(sample_path, file)
                    break
            
            # If both the JSON and S1P files exist, process the sample
            if os.path.exists(json_file) and s1p_file:
                # Read the JSON metadata
                metadata = read_json(json_file)
                
                # Skip if latitude or longitude are missing
                if not metadata.get('latitude') or not metadata.get('longitude'):
                    skipped_samples += 1
                    skipped_samples_names.append(sample_folder)  # Add folder name to skipped list
                    continue
                
                # Read the S1P data block as a string
                s1p_data = read_s1p(s1p_file)
                
                # Prepare the row for the sample
                row = {
                    'Timestamp': metadata['timestamp'],
                    'Latitude': metadata['latitude'],
                    'Longitude': metadata['longitude'],
                    'HeightLabel': metadata['heightLabel'],
                    'ShearVain20cm': metadata['shearVain20cm'],
                    'ShearVain50cm': metadata['shearVain50cm'],
                    'ShearVain80cm': metadata['shearVain80cm'],
                    'SurfaceWaterSubmerged': metadata['surfaceWaterSubmerged'],
                    'RecentScrollOver': metadata['recentScrollOver'],
                    'S1P_Data_Block': s1p_data
                }
                
                # Add the row to the list of rows
                rows.append(row)
    
    # Create a DataFrame from the rows
    df = pd.DataFrame(rows)
    
    # Write the DataFrame to a CSV file
    df.to_csv(output_csv, index=False)
    
    # Print the summary
    print(f"Total samples processed: {total_samples}")
    print(f"Total samples skipped: {skipped_samples}")
    print(f"Total rows in CSV: {len(df)}")
    
    # Print the names of the skipped samples
    if skipped_samples > 0:
        print("\nSkipped samples due to missing latitude/longitude:")
        for name in skipped_samples_names:
            print(name)

# Example usage:
# Folder containing subfolders for each sample
data_folder = r'C:\Users\JoshuaPaterson\Downloads\Data Processing Scripts\MT_WELD_OUTPUT'

# Output CSV file
output_csv = 'output_samples.csv'

# Create the CSV
create_csv(data_folder, output_csv)

print("CSV file created successfully!")