import pandas as pd
import numpy as np
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import joblib
import os

# Check if required files exist
if not os.path.exists('btc_model.keras'):
    raise FileNotFoundError("The model file 'btc_model.keras' was not found.")
if not os.path.exists('feature_scaler.pkl') or not os.path.exists('target_scaler.pkl'):
    raise FileNotFoundError("Scaler files were not found.")
if not os.path.exists('data/processed_data.csv'):
    raise FileNotFoundError("The data file 'data/processed_data.csv' was not found.")

# Load the model and scalers
model = load_model('btc_model.keras')
feature_scaler = joblib.load('feature_scaler.pkl')
target_scaler = joblib.load('target_scaler.pkl')

# Load and prepare new data
data = pd.read_csv('data/processed_data.csv')
data.set_index('Date', inplace=True)

# Assume new data for prediction is already processed and available as 'data'
features = data[['MA_7', 'MA_30', 'RSI', 'MACD']].values
features_scaled = feature_scaler.transform(features)

# Reshape input for prediction
features_scaled = features_scaled.reshape((features_scaled.shape[0], 1, features_scaled.shape[1]))

# Make predictions in batches (in case of large datasets)
batch_size = 1000  # Adjust this value based on memory capacity
predictions = []

for i in range(0, len(features_scaled), batch_size):
    batch_predictions = model.predict(features_scaled[i:i + batch_size])
    predictions.append(batch_predictions)

# Concatenate batch predictions
predictions = np.concatenate(predictions, axis=0)

# Inverse transform the predictions
predictions = target_scaler.inverse_transform(predictions)

# Save predictions to DataFrame
data['predicted_close'] = np.nan  # Initialize the column
data.loc[data.index[-len(predictions):], 'predicted_close'] = predictions.flatten()  # Use loc for assignment

# Save to CSV
output_file = 'data/predictions.csv'
data.to_csv(output_file)
print(f"Predictions saved to '{output_file}'.")
