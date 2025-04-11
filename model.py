import pandas as pd
import numpy as np
import json
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# Load dataset
data_path = r"E:\yieldwise\backend\Filtered_Dataset.csv"
try:
    data = pd.read_csv(data_path)
    print("Dataset loaded successfully.")
except Exception as e:
    print(f"Error loading dataset: {e}")
    exit()

# Standardize column names
data.columns = data.columns.str.strip().str.replace(" ", "_")

# Convert text columns to lowercase for consistency
data['Commodity'] = data['Commodity'].str.strip().str.lower()
data['State'] = data['State'].str.strip().str.lower()

# Function to prepare data
def prepare_data(data, commodity_name, state_name, min_records=10):
    filtered_data = data[(data['Commodity'] == commodity_name) & (data['State'] == state_name)]
    
    # Debugging output
    print(f"Filtered data for {commodity_name} in {state_name}: {len(filtered_data)} records found.")

    if len(filtered_data) < min_records:
        print(f"Warning: Only {len(filtered_data)} records found for {commodity_name} in {state_name}. Using simplified model.")
        return None, None, None  # Return None if not enough data

    features = filtered_data[['Avg_Price']].copy()
    
    # Add synthetic features
    features['Temperature'] = np.random.rand(len(features)) * 30
    features['Rainfall'] = np.random.rand(len(features)) * 100
    
    # Scale data
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(features)

    X, y = [], []
    time_step = 5  # Default time step
    for i in range(len(scaled_data) - time_step):
        X.append(scaled_data[i:i + time_step, :])
        y.append(scaled_data[i + time_step, 0])

    return np.array(X), np.array(y), scaler

# Initialize predictions dictionary
predictions = {}

# List of unique commodities and states
unique_commodities = data['Commodity'].unique()
unique_states = data['State'].unique()

# Loop through each commodity and state to generate predictions
for commodity_name in unique_commodities:
    for state_name in unique_states:
        # Prepare data for the current commodity and state
        X, y, scaler = prepare_data(data, commodity_name.lower(), state_name.lower())

        # Check if data is sufficient
        if X is None or y is None:
            print(f"Skipping {commodity_name} in {state_name} due to insufficient data.")
            continue  # Skip to the next iteration if there's not enough data

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Define model
        model = Sequential([
            LSTM(32, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])),
            Dropout(0.2),
            LSTM(32, return_sequences=False),
            Dropout(0.2),
            Dense(20, activation='relu'),
            Dense(1)
        ])

        model.compile(optimizer='adam', loss='mean_squared_error')

        # Train model
        model.fit(X_train, y_train, epochs=3, batch_size=8, validation_data=(X_test, y_test), verbose=1)

        # Predict
        test_input = X_test[-1].reshape(1, X_test.shape[1], X_test.shape[2])
        predicted_price = model.predict(test_input)
        predicted_price_original = scaler.inverse_transform(
            np.concatenate((predicted_price, np.zeros((predicted_price.shape[0], 2))), axis=1)
        )[:, 0]

        # Save prediction
        predictions[f"{commodity_name.lower()}_{state_name.lower()}"] = {
            "commodity": commodity_name.capitalize(),
            "state": state_name.capitalize(),
            "predicted_price": f"₹{predicted_price_original[0]:.2f}"
        }

# Save all predictions to JSON
with open("predictions.json", "w") as f:
    json.dump(predictions, f)

print("Predictions saved to predictions.json.") 