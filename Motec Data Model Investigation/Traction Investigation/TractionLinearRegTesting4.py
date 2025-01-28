import pandas as pd
import joblib  # Import joblib to load the saved model
from sklearn.preprocessing import LabelEncoder

# Function to load the cleaned data from CSV
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        print("CSV Loaded Successfully")
        return data
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None

# Function to preprocess the new data for prediction
def preprocess_data(data, scaler):
    # Select relevant columns for prediction (you can modify this as per your features)
    selected_columns = [
        'Average of Traction_Average', 
        'Average of Engine_Torque',
        'Average of GPS_Speed',
        'Sum of Engine_Temp', 
        'Sum of Traction_Diff_radio'
    ]
    
    # Check if any columns are missing
    missing_columns = [col for col in selected_columns if col not in data.columns]
    if missing_columns:
        print(f"Missing columns: {missing_columns}")
        return None, None

    # Prepare the feature set by selecting and dropping rows with missing values
    X = data[selected_columns].dropna()
    
    # Scale the features using the loaded scaler
    X_scaled = scaler.transform(X)
    
    # Return the scaled features and the corresponding indices
    return X_scaled, X.index

# Function to load the trained model
def load_model(model_path='linear_regression_model.pkl'):
    try:
        model = joblib.load(model_path)
        print("Model Loaded Successfully")
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

# Function to load the scaler
def load_scaler(scaler_path='scaler.pkl'):
    try:
        scaler = joblib.load(scaler_path)
        print("Scaler Loaded Successfully")
        return scaler
    except Exception as e:
        print(f"Error loading scaler: {e}")
        return None

# Function to make predictions and save results
def make_predictions_and_save(data, model, scaler, output_path):
    X_scaled, X_index = preprocess_data(data, scaler)
    
    if X_scaled is None:
        return
    
    # Make predictions
    y_pred = model.predict(X_scaled)
    
    # Divide the predicted values by 200
    y_pred_divided = y_pred
    
    print(y_pred_divided[0])
    
    # Create a DataFrame with the necessary output columns
    #result_df = data.loc[X_index, ['UTC adjusted datetime Column', 'GPS_Latitude', 'GPS_Longitude', 'Mud Condition']].copy()
    result_df = data.loc[X_index, ['UTC adjusted datetime Column', 'GPS_Latitude', 'GPS_Longitude']].copy()
    
    # Save the divided predictions to the 'Predicted Mud Condition' column
    result_df['Predicted Mud Condition'] = y_pred_divided
    
    # Save the results to a new CSV
    print(y_pred_divided[0])
    print(y_pred_divided[1])
    print(y_pred_divided[2])
    print(y_pred_divided[3])
    print(y_pred_divided[4])
    print(result_df.head())
    result_df.to_csv(output_path, index=False)
    print(f"Results saved to {output_path}")

# Main function to run the entire workflow
def main():
    # Path to the new data and the output file
    input_file = 'MM43 Data.csv'  # Input file path with new data for predictions
    output_file = 'MM43_predicted_mud_conditions.csv'  # Output file path for predictions
    
    # Load the new data for prediction
    data = load_data(input_file)
    if data is None:
        return
    
    # Load the trained model (already saved previously)
    model = load_model()
    if model is None:
        return
    
    # Load the scaler (saved previously)
    scaler = load_scaler()
    if scaler is None:
        return
    
    # Make predictions and save the results
    make_predictions_and_save(data, model, scaler, output_file)

if __name__ == "__main__":
    main()