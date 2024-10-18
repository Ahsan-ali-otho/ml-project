from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS
import pandas as pd
import numpy as np
import logging
from tabulate import tabulate
import requests  # Import requests to fetch historical prices

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)

def get_historical_prices():
    # Example of fetching historical Bitcoin prices (adjust the URL as needed)
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=365"
    response = requests.get(url)
    data = response.json()

    # Check if the 'prices' key is present in the API response
    if 'prices' in data:
        prices = [(pd.to_datetime(date[0], unit='ms'), date[1]) for date in data['prices']]  # Adjust to extract date
        return pd.DataFrame(prices, columns=['Date', 'Actual Price'])
    else:
        # Log the issue and return an empty DataFrame if 'prices' key is missing
        logging.error("'prices' key not found in the API response.")
        return pd.DataFrame(columns=['Date', 'Actual Price'])

def get_current_btc_price():
    # Fetch the current Bitcoin price
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data['bitcoin']['usd'] if 'bitcoin' in data else None  # Ensure 'bitcoin' key exists

# Dummy data for demonstration (simulate the next 10 days of predictions)
def generate_predictions(days=10):
    dates = pd.date_range(start=pd.Timestamp.now(), periods=days, freq='D')  # Start from today
    predicted_prices = np.random.rand(days) * 1000  # Simulating random prices
    percentage_change = ((predicted_prices - np.mean(predicted_prices)) / np.mean(predicted_prices)) * 100  # Simulated % change
    volatility = np.std(predicted_prices)  # Volatility as the standard deviation

    return pd.DataFrame({
        'Date': dates,
        'Predicted Price': predicted_prices,
        'Percentage Change (%)': percentage_change,
        'Volatility': [volatility] * days  # Same volatility value for each prediction
    })

@app.route('/predict', methods=['GET'])
def predict():
    # Get the current price of Bitcoin
    current_btc_price = get_current_btc_price()
    if current_btc_price is None:
        return jsonify({'error': 'Unable to fetch current Bitcoin price.'}), 500

    # Generate predictions for the next 10 days
    short_term_predictions = generate_predictions(10)

    # Generate predictions for the next year (365 days)
    long_term_predictions = generate_predictions(365)

    # Get actual historical prices for the past year
    historical_prices = get_historical_prices()

    # Log short-term predictions in a table format
    logging.info("Short-term Predicted Prices:\n%s", tabulate(short_term_predictions, headers='keys', tablefmt='pretty'))

    # Calculate advice based on short-term predictions
    advice, predicted_trend = calculate_advice(short_term_predictions['Predicted Price'], current_btc_price)

    # Calculate absolute mean for short-term predictions
    absolute_mean = np.mean(np.abs(short_term_predictions['Predicted Price']))

    # Simulate actual prices for error calculation
    actual_prices = np.random.rand(10) * 1000  # Simulate actual prices for error calculation
    mae = np.mean(np.abs(short_term_predictions['Predicted Price'] - actual_prices))
    mse = np.mean((short_term_predictions['Predicted Price'] - actual_prices) ** 2)

    # Calculate target price based on the last predicted price and the trend
    target_price = calculate_target_price(short_term_predictions['Predicted Price'], predicted_trend)

    return jsonify({
        'current_price': f"${current_btc_price:.2f} USD",  # Add the current price to the response
        'predictions': short_term_predictions.to_dict(orient='records'),
        'advice': advice,
        'absolute_mean': absolute_mean,
        'mae': mae,
        'mse': mse,
        'predicted_trend': predicted_trend,
        'target_price': target_price,
        'long_term_predictions': long_term_predictions.to_dict(orient='records'),
        'historical_prices': historical_prices.to_dict(orient='records')  # Include historical prices
    })

def calculate_advice(predicted_prices, current_price):
    # Determine trend based on the first and last predicted prices compared to the current price
    predicted_price = predicted_prices.iloc[0]  # Take the next day's predicted price
    if predicted_price > current_price:  # Prices are expected to rise
        trend = "upward"
        return "Buy: Prices are predicted to rise.", trend
    else:  # Prices are expected to fall
        trend = "downward"
        return "Sell: Prices are predicted to fall.", trend

def calculate_target_price(predicted_prices, trend):
    # Calculate target price as a simple projection based on the last price and the predicted trend
    if trend == "upward":
        return round(predicted_prices.iloc[-1] * 1.10, 2)  # Increase by 10%
    else:
        return round(predicted_prices.iloc[-1] * 0.90, 2)  # Decrease by 10%

if __name__ == '__main__':
    app.run(debug=True)
