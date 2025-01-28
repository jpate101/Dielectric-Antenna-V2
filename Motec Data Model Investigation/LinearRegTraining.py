# ---------------------------------------------------------------
# Linear Regression Model for Mud Condition Prediction
# ---------------------------------------------------------------
#
# This script builds a linear regression model to predict the mud condition 
# based on vehicle performance data such as traction, engine torque, GPS speed, 
# and other relevant features. The model is trained on a cleaned dataset with 
# historical mud condition data, and the following steps are performed:
#
# 1. Load the cleaned dataset from a CSV file.
# 2. Prepare the data by selecting relevant features and the target variable 
#    ('Mud Condition').
# 3. Apply SMOTE (Synthetic Minority Over-sampling Technique) to handle class 
#    imbalance in the dataset.
# 4. Split the data into training and testing sets.
# 5. Scale the features using StandardScaler to normalize the data for better 
#    model performance.
# 6. Train a linear regression model on the resampled and scaled training data.
# 7. Evaluate the model's performance using Mean Squared Error (MSE) and 
#    R-squared (R2) score.
# 8. Save the trained model and scaler using joblib.
# 9. Use the trained model and scaler to predict mud conditions on new data.
# 10. Save the predicted results to a new CSV file.
#
# This process enables the prediction of mud conditions for new data based on 
# the relationships learned from the historical dataset.
#
# Input: Cleaned dataset (CSV) containing features like traction, engine torque,
#        GPS speed, etc.
# Output: Predictions of mud conditions along with original data in a new CSV file.
#

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from imblearn.over_sampling import SMOTE  # Import SMOTE for oversampling
import joblib  # Import joblib to save the model
from sklearn.preprocessing import StandardScaler

# Function to load cleaned data from CSV
def load_cleaned_data(file_path):
    try:
        data = pd.read_csv(file_path)
        print("Cleaned CSV Loaded Successfully")
        return data
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None

# Function to prepare the data (features and target)
def prepare_data(data):
    if 'Mud Condition' not in data.columns:
        print("'Mud Condition' column not found in the dataset.")
        return None, None
    
    # Specify the columns you want to use as features
    selected_columns = [
        'Average of Traction_Average', 
        'Average of Engine_Torque',
        'Average of GPS_Speed',
        'Sum of Traction_Diff_radio',
#        'Sum of Engine_Temp'
    ]
    
    # Ensure these columns exist in the data
    missing_columns = [col for col in selected_columns if col not in data.columns]
    if missing_columns:
        print(f"Missing columns: {missing_columns}")
        return None, None

    # Prepare the features (X) and target (y)
    X = data[selected_columns]
    y = data['Mud Condition']
    
    # Drop rows with NaN values in the feature set
    X = X.dropna()
    y = y[X.index]  # Ensure target variable y matches X's cleaned index
    
    # Apply SMOTE to balance the classes (oversample the minority class)
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)
    
    print(f"Original data size: {X.shape[0]} samples")
    print(f"Resampled data size: {X_resampled.shape[0]} samples")
    
    return X_resampled, y_resampled

# Function to scale the features
def scale_features(X_train, X_test):
    # Initialize the scaler
    scaler = StandardScaler()
    
    # Fit the scaler on the training data and transform it
    X_train_scaled = scaler.fit_transform(X_train)
    
    # Apply the same transformation to the test data
    X_test_scaled = scaler.transform(X_test)
    
    # Save the scaler for later use
    joblib.dump(scaler, 'scaler.pkl')
    print("\nScaler saved to 'scaler.pkl'")
    
    return X_train_scaled, X_test_scaled, scaler

# Function to perform linear regression
def perform_linear_regression(X, y):
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15)

    # Scale the features
    X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)

    # Initialize and fit the model
    model = LinearRegression()
    model.fit(X_train_scaled, y_train)

    # Predictions on the test set
    y_pred = model.predict(X_test_scaled)

    # Performance metrics
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Displaying performance and coefficients
    print("Linear Regression Model Performance:")
    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")

    # Feature weights (coefficients)
    coef_df = pd.DataFrame(model.coef_, X.columns, columns=['Coefficient'])
    print("\nFeature Weights (Coefficients):")
    print(coef_df)

    # Intercept (bias term)
    print(f"\nIntercept (Bias term): {model.intercept_}")

    # Save the model to a file
    joblib.dump(model, 'linear_regression_model.pkl')
    print("\nModel saved to 'linear_regression_model.pkl'")

    return model, y_pred, y_test, scaler

# Function to preprocess and scale the new data for prediction
def preprocess_and_scale_data(data, scaler):
    # Select relevant columns for prediction
    selected_columns = [
        'Average of Traction_Average', 
        'Average of Engine_Torque',
        'Average of GPS_Speed',
        'Sum of Traction_Diff_radio',
#        'Sum of Engine_Temp'
    ]
    
    # Check if the required columns are available
    if not all(col in data.columns for col in selected_columns):
        print(f"Missing columns: {selected_columns}")
        return None
    
    # Prepare the features for prediction
    X = data[selected_columns].dropna()

    # Scale the features using the saved scaler
    X_scaled = scaler.transform(X)
    
    return X_scaled

# Function to make predictions and save results
def make_predictions_and_save(data, model, scaler, output_path):
    X_scaled = preprocess_and_scale_data(data, scaler)
    
    if X_scaled is None:
        return
    
    # Make predictions
    y_pred = model.predict(X_scaled)
    
    # Save the predictions to a DataFrame and then to a CSV file
    result_df = data.copy()
    result_df['Predicted Mud Condition'] = y_pred
    result_df.to_csv(output_path, index=False)
    print(f"Predictions saved to {output_path}")

# Main function to run the entire workflow
def main():
    # Load the cleaned data
    file_path = 'MM23_13-17_012025/MM23 Data WithMudconditions.csv'  # Path to cleaned data
    data = load_cleaned_data(file_path)
    
    if data is None:
        return

    # Print the number of rows in the training data
    print(f"Number of rows in the training data: {len(data)}")
    
    # Prepare the features and target variable, now with resampling
    X_resampled, y_resampled = prepare_data(data)
    
    if X_resampled is None or y_resampled is None:
        return

    # Perform linear regression on the resampled data
    model, y_pred, y_test, scaler = perform_linear_regression(X_resampled, y_resampled)
    
    # Step 2: Use the trained model and scaler to make predictions on new data
    input_file = file_path  # Path to new data
    output_file = 'MM23_13-17_012025/MM23_Predictions.csv'  # Path to save predictions
    
    # Load the new data
    data = load_cleaned_data(input_file)
    
    if data is None:
        return
    
    # Load the trained model and scaler
    model = joblib.load('linear_regression_model.pkl')
    scaler = joblib.load('scaler.pkl')
    print("Model and scaler loaded successfully")

    # Make predictions and save the results
    make_predictions_and_save(data, model, scaler, output_file)

if __name__ == "__main__":
    main()
