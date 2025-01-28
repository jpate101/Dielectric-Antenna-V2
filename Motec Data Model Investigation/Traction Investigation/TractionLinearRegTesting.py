import pandas as pd

def load_data(file_path):
    """
    Loads data from a CSV file.
    """
    try:
        data = pd.read_csv(file_path)
        print("CSV Loaded Successfully")
        return data
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None

def remove_unwanted_columns(data):
    """
    Remove specified unwanted columns.
    """
    #'Average of Traction_Average', 'Average of Engine_Torque','Average of GPS_Speed'
    columns_to_remove = [
        'UTC adjusted datetime Column', 'GPS_Latitude', 'GPS_Longitude', 'Sum of Every1000thRow', 'Vehicle_Id',
        'Sum of BEARING_PRESSURE_LEFT_DRIVE', 'Sum of BEARING_PRESSURE_RIGHT_DRIVE',
        'Sum of Engine_Hours__ECU_', 'Sum of Scroll_Speed_Difference',
        'Year', 'Quarter', 'Month', 'Day',
        'Quarter.1', 'Month.1', 'Day.1',
        'Year.2', 'Quarter.2', 'Month.2', 'Day.2',
        'Year.3', 'Quarter.3', 'Month.3', 'Day.3',
        'Year.4', 'Quarter.4', 'Month.4', 'Day.4',
        'Time Video Column', 'Time second', 'Time minute', 'Time hour', 
        'Time Column', 'Sum of Time',
        'Log_Date', 'X devidelineTimeWetBegin','Year.1'  
    ]
    return data.drop(columns=columns_to_remove, errors='ignore')

def convert_columns_to_float(data):
    """
    Converts all columns except 'Mud Condition' to float, if possible.
    """
    for col in data.columns:
        if col != 'Mud Condition':  # Skip the Mud Condition column
            try:
                data[col] = pd.to_numeric(data[col], errors='raise')  # raise error if fails
            except ValueError:
                # If conversion fails, print the column name
                print(f"Column '{col}' contains non-numeric values and cannot be converted to float.")
    return data

def process_mud_condition(data):
    """
    Process the 'Mud Condition' column:
    - Remove rows with 'Unknown'
    - Convert mud condition categories to numeric values (0-4)
    """
    # Remove rows where 'Mud Condition' is 'Unknown'
    data_cleaned = data[data['Mud Condition'] != 'Unknown']
    
    # Map the Mud Condition to numeric values
    mud_condition_map = {
        'Water/Loose (10%)': 0,
        'Sticky (30%)': 1,
        'Good Run (50%)': 2,
        'Dry (70%)': 3,
        'Super Dry (90%)': 4
    }
    
    data_cleaned['Mud Condition'] = data_cleaned['Mud Condition'].map(mud_condition_map)
    
    return data_cleaned

def save_data(data, file_name):
    """
    Save DataFrame to CSV.
    """
    try:
        data.to_csv(file_name, index=False)
        print(f"Data saved to {file_name}")
    except Exception as e:
        print(f"Error saving CSV: {e}")

def main():
    """
    Main function to load data, remove unwanted columns, clean 'Mud Condition', and save cleaned data.
    """
    # Load the CSV file
    file_path = 'output_with_mud_condition.csv'  # Change this path to your file
    data = load_data(file_path)
    
    if data is None:
        return

    # Print the columns before removing unwanted columns
    print("Original Columns in DataFrame:")
    print(data.columns.tolist())
    
    # Remove unwanted columns
    data_cleaned = remove_unwanted_columns(data)

    # Process the Mud Condition column (remove 'Unknown' and map to numeric)
    data_cleaned = process_mud_condition(data_cleaned)

    # Convert the other columns to float (except 'Mud Condition')
    data_cleaned = convert_columns_to_float(data_cleaned)

    # Save the cleaned data to a new CSV
    save_data(data_cleaned, 'training_clean_data.csv')

    print("\nProcessed data saved successfully!")

if __name__ == "__main__":
    main()