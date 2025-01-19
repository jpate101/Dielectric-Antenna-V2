import os
import shutil
import json
import csv
from datetime import datetime, timedelta

# Paths to your folder locations
json_folder = r'C:\Users\JoshuaPaterson\Phibion Pty Ltd\IG88 - General\03 Development\Dielectric Antenna\Predictive Model Training Guide and FIles\Data Labeling Scripts\Mt Weld Data D2'
s1p_folder = r'C:\Users\JoshuaPaterson\Phibion Pty Ltd\IG88 - General\03 Development\Dielectric Antenna\Predictive Model Training Guide and FIles\Data Labeling Scripts\Mt Weld S1P - Day 2\S1P Merge'
output_folder = r'C:\Users\JoshuaPaterson\Phibion Pty Ltd\IG88 - General\03 Development\Dielectric Antenna\Predictive Model Training Guide and FIles\Data Labeling Scripts\MT_WELD_D2_OUTPUT'
csv_file = r'C:\Users\JoshuaPaterson\Phibion Pty Ltd\IG88 - General\03 Development\Dielectric Antenna\Predictive Model Training Guide and FIles\Data Labeling Scripts\Mt Weld S1P - Day 2\CSV_D2_Merge-WINJAMAICA-NS.csv'

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Counters for used and skipped files
used_files_count = 0
skipped_files_count = 0

# Read CSV and build a dictionary for quick lookup by vna_filename
csv_data = {}
with open(csv_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        vna_filename = row['vna_filename']
        gps_data = {
            'latitude': row['latitude'],
            'longitude': row['longitude']
        }
        csv_data[vna_filename] = gps_data

# Function to convert timestamp to the format in the s1p filenames
def convert_timestamp_to_filename_format(timestamp):
    dt_obj = datetime.fromisoformat(timestamp)  # Parse the ISO format timestamp
    return dt_obj.strftime('%Y-%m-%dT%H-%M-%S') + '.' + timestamp.split('.')[-1] + 'Z'

# Function to check if the timestamps are within a 30-second margin
def is_within_margin(json_timestamp, s1p_timestamp, margin_seconds=20):
    s1p_timestamp = s1p_timestamp.rstrip('Z')  # Remove 'Z' if it exists

    # Ensure the timestamp is properly formatted with up to microseconds
    if len(s1p_timestamp) > 26:
        s1p_timestamp = s1p_timestamp[:26]  # Only keep the first 6 digits for microseconds

    # Convert both JSON and S1P timestamps to datetime objects
    try:
        
        json_time = datetime.strptime(json_timestamp, '%Y-%m-%dT%H:%M:%S.%f')
        s1p_time = datetime.strptime(s1p_timestamp, '%Y-%m-%dT%H-%M-%S.%f')  # Correct S1P timestamp format
        
        #s1p_time = s1p_time + timedelta(hours=10)
        
        #print(json_time)
        #print(s1p_time)
        
    except ValueError as e:
        print(f"Error parsing timestamps: {json_timestamp} and {s1p_timestamp}. Error: {e}")
        return False  # If we can't parse, return False (they don't match)

    # Calculate the time difference in seconds
    time_diff = abs((json_time - s1p_time).total_seconds())
    
    return time_diff <= margin_seconds

# Process the JSON files
for json_file_name in os.listdir(json_folder):
    if json_file_name.endswith('.json'):
        json_file_path = os.path.join(json_folder, json_file_name)
        
        # Open the JSON file and load its contents
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        
        # Extract the timestamp from the JSON file
        json_timestamp = data.get('timestamp', '')
        
        # Print the timestamp of the current JSON file
        print(f"Processing JSON file: {json_file_name} with timestamp: {json_timestamp}")
        
        # Convert the timestamp into the format used in the s1p filename
        s1p_filename_base = convert_timestamp_to_filename_format(json_timestamp)
        
        # Search for corresponding S1P files with a 30-second margin
        s1p_found = False
        for s1p_file_name in os.listdir(s1p_folder):
            if s1p_file_name.endswith('.s1p'):
                s1p_file_path = os.path.join(s1p_folder, s1p_file_name)
                
                # Extract the timestamp portion from the S1P filename (assumed to be at the start)
                s1p_timestamp_str = s1p_file_name.split('_')[0]  # Extract timestamp from the filename
                
                # Check if the timestamps are within the margin
                if is_within_margin(json_timestamp, s1p_timestamp_str):
                    # If the timestamps are within 30 seconds, copy both files
                    
                    # Create a new folder for the matching files
                    new_folder = os.path.join(output_folder, os.path.splitext(json_file_name)[0])
                    os.makedirs(new_folder, exist_ok=True)
                    
                    # Copy the JSON file as 'data.json'
                    shutil.copy(json_file_path, os.path.join(new_folder, 'data.json'))
                    
                    # Get the corresponding GPS data from the CSV file
                    gps_data = csv_data.get(s1p_file_name, None)
                    
                    if gps_data:
                        # Update the JSON data with GPS info
                        with open(os.path.join(new_folder, 'data.json'), 'r') as f:
                            json_data = json.load(f)
                        
                        json_data.update(gps_data)
                        
                        # Save the updated data to data.json
                        with open(os.path.join(new_folder, 'data.json'), 'w') as f:
                            json.dump(json_data, f, indent=4)
                    
                    # Copy the S1P file
                    shutil.copy(s1p_file_path, new_folder)
                    
                    print(f"Copied: {json_file_name} (renamed to data.json) and {s1p_file_name} to {new_folder}")
                    
                    s1p_found = True
                    used_files_count += 1  # Increment the used files counter
                    break
        
        if not s1p_found:
            print(f"Skipping {json_file_name}: No corresponding S1P file found within 20 seconds")
            skipped_files_count += 1  # Increment the skipped files counter

# Print the final count of used and skipped files
print(f"\nTotal used files: {used_files_count}")
print(f"Total skipped files: {skipped_files_count}")