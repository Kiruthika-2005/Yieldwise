import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input
import os

# Load the dataset
df = pd.read_csv(r"C:\Users\Dell\Downloads\vegetable_sales_growth_2013_2024.csv")
df['Month'] = df['Month'].astype(int)

# Define model directory for VS Code
model_dir = "vegetable_models"
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

# Prepare LSTM data
def prepare_lstm_data(series, time_steps=12):
    dataX, dataY = [], []
    for i in range(len(series) - time_steps):
        a = series[i:(i + time_steps)]
        dataX.append(a)
        dataY.append(series[i + time_steps])
    return np.array(dataX), np.array(dataY)

# Train and save models for all vegetables
vegetables = df['Vegetable'].unique()
for vegetable in vegetables:
    veg_data = df[df['Vegetable'] == vegetable].copy()
    veg_data = veg_data.sort_values(by=['Year', 'Month']).reset_index(drop=True)

    # Train for Quantity_Sold
    quantity_series = veg_data['Quantity_Sold'].values
    scaler_q = MinMaxScaler()
    quantity_scaled = scaler_q.fit_transform(quantity_series.reshape(-1, 1))
    X_q, y_q = prepare_lstm_data(quantity_scaled)

    model_q = Sequential([
        Input(shape=(X_q.shape[1], 1)),
        LSTM(30, return_sequences=False),
        Dense(1)
    ])
    model_q.compile(loss='mean_squared_error', optimizer='adam')
    model_q.fit(X_q.reshape(X_q.shape[0], X_q.shape[1], 1), y_q, epochs=5, batch_size=16, verbose=1)

    # Save quantity model and scaler
    model_q.save(f"{model_dir}/{vegetable}_quantity_model.keras")
    np.save(f"{model_dir}/{vegetable}_quantity_scaler.npy", scaler_q)

    # Train for Growth
    growth_series = veg_data['Growth'].values
    scaler_g = MinMaxScaler()
    growth_scaled = scaler_g.fit_transform(growth_series.reshape(-1, 1))
    X_g, y_g = prepare_lstm_data(growth_scaled)

    model_g = Sequential([
        Input(shape=(X_g.shape[1], 1)),
        LSTM(30, return_sequences=False),
        Dense(1)
    ])
    model_g.compile(loss='mean_squared_error', optimizer='adam')
    model_g.fit(X_g.reshape(X_g.shape[0], X_g.shape[1], 1), y_g, epochs=5, batch_size=16, verbose=1)

    # Save growth model and scaler
    model_g.save(f"{model_dir}/{vegetable}_growth_model.keras")
    np.save(f"{model_dir}/{vegetable}_growth_scaler.npy", scaler_g)

print("✅ Models trained and saved for all vegetables!")

# --- Prediction for Selected Vegetable ---

from tensorflow.keras.models import load_model

def predict_for_vegetable(selected_vegetable):
    try:
        # Load models and scalers
        model_q = load_model(f"{model_dir}/{selected_vegetable}_quantity_model.keras")
        scaler_q = np.load(f"{model_dir}/{selected_vegetable}_quantity_scaler.npy", allow_pickle=True).item()

        model_g = load_model(f"{model_dir}/{selected_vegetable}_growth_model.keras")
        scaler_g = np.load(f"{model_dir}/{selected_vegetable}_growth_scaler.npy", allow_pickle=True).item()

    except Exception as e:
        print(f"❌ Error: {e}")
        return

    # Get latest data for prediction
    veg_data = df[df['Vegetable'] == selected_vegetable].copy()
    veg_data = veg_data.sort_values(by=['Year', 'Month']).reset_index(drop=True)

    quantity_series = veg_data['Quantity_Sold'].values
    quantity_scaled = scaler_q.transform(quantity_series.reshape(-1, 1))

    growth_series = veg_data['Growth'].values
    growth_scaled = scaler_g.transform(growth_series.reshape(-1, 1))

    # Predict next 12 months
    future_quantity_preds, future_growth_preds = [], []
    last_sequence_q = quantity_scaled[-12:].tolist()
    last_sequence_g = growth_scaled[-12:].tolist()

    for _ in range(12):
        pred_q = model_q.predict(np.array(last_sequence_q[-12:]).reshape(1, 12, 1), verbose=0)
        last_sequence_q.append(pred_q[0])
        future_quantity_preds.append(scaler_q.inverse_transform(pred_q)[0][0])

        pred_g = model_g.predict(np.array(last_sequence_g[-12:]).reshape(1, 12, 1), verbose=0)
        last_sequence_g.append(pred_g[0])
        future_growth_preds.append(scaler_g.inverse_transform(pred_g)[0][0])

    # Plot predictions
    future_months = ["Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb"]
    x = np.arange(len(future_months))
    width = 0.35

    plt.figure(figsize=(14, 6))
    plt.bar(x - width/2, future_quantity_preds, width, label='Predicted Quantity Sold', color='#006400')
    plt.bar(x + width/2, future_growth_preds, width, label='Predicted Growth Level', color='#90EE90')
    plt.xlabel('Months')
    plt.ylabel('Values')
    plt.title(f'12-Month Prediction for {selected_vegetable} (Mar to next Feb)')
    plt.xticks(x, future_months)
    plt.legend()
    plt.grid(axis='y')

    # Save graph and display
    plt.savefig(f"{selected_vegetable}_prediction_graph.png")
    plt.show()
    plt.close()

for veg in vegetables:
    predict_for_vegetable(veg)1