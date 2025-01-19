# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 07:59:44 2024

@author: JoshuaPaterson
"""

import os
import json

def combine_json_files(base_folder, output_file):
    combined_data = []

    # Traverse the directory structure
    for root, dirs, files in os.walk(base_folder):
        for file in files:
            if file == 'data.json':
                # Get the full path to the data.json file
                data_file_path = os.path.join(root, file)
                
                # Read the JSON data from the file
                with open(data_file_path, 'r') as f:
                    try:
                        data = json.load(f)
                        combined_data.append(data)
                    except json.JSONDecodeError as e:
                        print(f"Error reading {data_file_path}: {e}")
    
    # Write the combined data to the output file
    with open(output_file, 'w') as out_file:
        # The combined data should be a valid JSON array, so wrap it in brackets and separate the items with commas
        json.dump(combined_data, out_file, indent=4)

    print(f"Data successfully combined into {output_file}")


if __name__ == "__main__":
    # Define the base folder where your data files are located
    base_folder = 'MT_WELD_OUTPUT'  # Update this path to your folder

    # Define the output file where the combined JSON data will be saved
    output_file = 'combined_data.json'  # Specify your desired output file name

    # Combine the JSON files
    combine_json_files(base_folder, output_file)