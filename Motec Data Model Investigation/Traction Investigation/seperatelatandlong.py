# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 12:34:20 2025

@author: JoshuaPaterson
"""

import csv
import re

# Function to convert GPS coordinate string to separate lat/long columns
def parse_gps(gps_str):
    # Regex to capture both the lat and long, with the potential for "S" or "E" suffixes
    lat_long_regex = r"([+-]?\d+\.\d+)(°\s?[NS])?,\s?([+-]?\d+\.\d+)(°\s?[EW])?"
    
    match = re.match(lat_long_regex, gps_str.strip())
    
    if match:
        lat_value = float(match.group(1))
        long_value = float(match.group(3))
        
        # Adjust for S or E direction if needed (negative for South or West)
        if 'S' in match.group(2):
            lat_value = -lat_value
        if 'W' in match.group(4):
            long_value = -long_value
        
        return lat_value, long_value
    else:
        # Return None if format doesn't match (invalid data)
        return None, None

# Function to process CSV
def process_csv(input_csv, output_csv):
    with open(input_csv, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['Latitude', 'Longitude']
        
        rows = []
        for row in reader:
            # Extract and parse the GPS coordinates
            gps_str = row['Default GPS']
            
            # If the format is the decimal type (e.g., -12.94828687, 141.64065592)
            if ',' in gps_str:
                lat_str, long_str = gps_str.split(',')
                try:
                    lat_value = float(lat_str.strip())
                    long_value = float(long_str.strip())
                    row['Latitude'] = lat_value
                    row['Longitude'] = long_value
                except ValueError:
                    row['Latitude'] = None
                    row['Longitude'] = None
            else:
                # Otherwise, parse the DMS format (e.g., 12.95241° S, 141.63323° E)
                lat_value, long_value = parse_gps(gps_str)
                row['Latitude'] = lat_value
                row['Longitude'] = long_value
                
            rows.append(row)

    # Write the updated CSV
    with open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"CSV has been processed and saved to {output_csv}")

# Example usage
input_csv = 'Vane Shear Report.csv'  # Replace with your input CSV file path
output_csv = 'Vane Shear Report2.csv'  # Replace with desired output CSV file path

process_csv(input_csv, output_csv)