import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from imblearn.over_sampling import SMOTE  # Import SMOTE for oversampling

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
    
    # Prepare the features and target
    X = data.drop(columns=['Mud Condition'], errors='ignore')
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

# Function to perform linear regression
def perform_linear_regression(X, y):
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15)

    # Initialize and fit the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predictions on the test set
    y_pred = model.predict(X_test)

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

    return model, y_pred, y_test

# Function to display number of samples per Mud Condition label
def display_label_distribution(y):
    print("\nNumber of samples for each 'Mud Condition' label:")
    print(y.value_counts())

def main():
    # Load the cleaned data
    file_path = 'training_clean_data.csv'  # Path to cleaned data
    data = load_cleaned_data(file_path)
    
    if data is None:
        return

    # Print the number of rows in the training data
    print(f"Number of rows in the training data: {len(data)}")
    
    # Prepare the features and target variable, now with resampling
    X_resampled, y_resampled = prepare_data(data)
    
    if X_resampled is None or y_resampled is None:
        return

    # Display number of samples per Mud Condition label in the resampled data
    display_label_distribution(y_resampled)
    
    # Perform linear regression on the resampled data
    model, y_pred, y_test = perform_linear_regression(X_resampled, y_resampled)
    
    # Display predictions vs true values
    results_df = pd.DataFrame({'True Values': y_test, 'Predictions': y_pred})
    print("\nPredictions vs True Values:")
    print(results_df.head())

if __name__ == "__main__":
    main()