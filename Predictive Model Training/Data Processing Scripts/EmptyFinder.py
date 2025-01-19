# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 08:37:06 2024

@author: JoshuaPaterson
"""

import os
import json

def find_empty_labels_and_output_timestamps(base_folder):
    # List to store timestamps with empty labels
    timestamps_with_empty_labels = []

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
                        # Check if the 'label' field is empty (i.e., "")
                        if data.get("shearVain20cm", "").strip() == "":
                            # If label is empty, collect the timestamp
                            timestamps_with_empty_labels.append(data.get("timestamp", "No Timestamp"))
                    except json.JSONDecodeError as e:
                        print(f"Error reading {data_file_path}: {e}")

    # Output the collected timestamps
    if timestamps_with_empty_labels:
        print("Timestamps for data with empty labels:")
        for timestamp in timestamps_with_empty_labels:
            print(timestamp)
    else:
        print("No entries with empty labels found.")

if __name__ == "__main__":
    # Define the base folder where your data files are located
    base_folder = 'MT_WELD_OUTPUT'  # Update this path to your folder

    # Find and output timestamps for entries with empty labels
    find_empty_labels_and_output_timestamps(base_folder)