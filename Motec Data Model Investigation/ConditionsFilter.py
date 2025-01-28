# ---------------------------------------------------------------
# Mud Condition Classification Script
# ---------------------------------------------------------------
#
# This script processes a CSV file containing vehicle performance data,
# specifically traction, engine torque, and GPS speed. Based on these 
# values, the script classifies each row into one of several predefined 
# "mud conditions" (e.g., Water/Loose, Sticky, Dry, etc.). Each mud 
# condition is associated with a numeric code (0 to 4), and the script 
# assigns this numeric code to a new column in the CSV file. 
# 
# The script also keeps track of the number of occurrences of each 
# mud condition and prints out the counts after processing all the rows.
#
# The following steps are performed:
# 1. Reads input CSV containing traction, torque, and GPS speed data.
# 2. Classifies each row into a mud condition based on predefined rules.
# 3. Adds a new column with the numeric mud condition code.
# 4. Counts and displays the number of occurrences of each mud condition.
# 5. Writes the updated data to a new CSV file with the mud condition column.
#
# Input CSV: Contains columns for "Average of Traction_Average", 
#             "Average of Engine_Torque", "Average of GPS_Speed".
# Output CSV: Same data with an additional "Mud Condition" column.

import csv

# Mud condition rules based on the provided criteria
mud_conditions = {
    "Water/Loose (10%)": {'traction': 80, 'torque': 35, 'gps_speed': 3, 'condition_number': 0},
    "Sticky (30%)": {'traction': 45, 'torque': 50, 'gps_speed': 1.3, 'condition_number': 1},
    "Good Run (50%)": {'traction': 83, 'torque': 60, 'gps_speed': 3.2, 'condition_number': 2},
    "Dry (70%)": {'traction': 95, 'torque': 85, 'gps_speed': 3.7, 'condition_number': 3},
    "Super Dry (90%)": {'traction': 95, 'torque': 90, 'gps_speed': 2.5, 'condition_number': 4}
}

# Function to determine mud condition based on Traction, Torque, and GPS Speed
def get_mud_condition(traction, torque, gps_speed):
    for condition, values in mud_conditions.items():
        if (abs(traction - values['traction']) <= 8 and 
            abs(torque - values['torque']) <= 8 and
            abs(gps_speed - values['gps_speed']) <= .9):
            return values['condition_number'], condition  # Return both number and name
    return -1, 'Unknown'  # Return -1 for 'Unknown' condition and name

# Function to process the CSV and add the 'Mud Condition' column
def process_csv(file_path, output_path):
    mud_condition_counts = {  # Keep names for counting
        "Water/Loose (10%)": 0, 
        "Sticky (30%)": 0, 
        "Good Run (50%)": 0, 
        "Dry (70%)": 0, 
        "Super Dry (90%)": 0, 
        "Unknown": 0
    }
    
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8-sig') as infile:
            csv_reader = csv.DictReader(infile)
            fieldnames = csv_reader.fieldnames + ['Mud Condition']  # Add new column 'Mud Condition'
            
            # Print headers to console
            print("CSV Headers:")
            print(", ".join(fieldnames))  # Join headers with commas and print
            
            rows = []
            
            # Process each row in the CSV
            for row in csv_reader:
                traction = float(row['Average of Traction_Average'])  # assuming 'Average of Traction_Average' contains the traction values
                torque = float(row['Average of Engine_Torque'])  # assuming 'Average of Engine_Torque' contains the torque values
                gps_speed = float(row['Average of GPS_Speed'])  # assuming 'Average of GPS_Speed' contains the GPS speed values
                
                mud_condition_number, mud_condition_name = get_mud_condition(traction, torque, gps_speed)
                row['Mud Condition'] = mud_condition_number  # Store the numeric mud condition in the CSV
                mud_condition_counts[mud_condition_name] += 1  # Increment the count for the mud condition name
                
                rows.append(row)
        
        # Write the modified rows to a new CSV file
        with open(output_path, mode='w', newline='', encoding='utf-8') as outfile:
            csv_writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            csv_writer.writeheader()
            csv_writer.writerows(rows)
        
        # Print the count of each mud condition to the console
        print("\nMud Condition Counts:")
        for condition, count in mud_condition_counts.items():
            print(f"{condition}: {count}")
    
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
file_path = 'MM23_13-17_012025/MM23 Data.csv'  # Replace with the path to your input CSV file
output_path = 'MM23_13-17_012025/MM23 Data WithMudconditions.csv'  # Path to save the output CSV
process_csv(file_path, output_path)