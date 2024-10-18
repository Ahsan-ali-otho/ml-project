import pandas as pd
import os

# Check if the input data file exists
input_file = 'data/btc_data.csv'
if not os.path.exists(input_file):
    raise FileNotFoundError(f"The input file '{input_file}' was not found.")

# Load the data
data = pd.read_csv(input_file)

# Print the first few rows and the columns of the DataFrame for debugging
print("Initial Data Preview:")
print(data.head())
print("Columns in the DataFrame:")
print(data.columns)

# Strip whitespace from column names (if any)
data.columns = data.columns.str.strip()

# Check if required columns are present
required_columns = ['Date', 'Close']
for col in required_columns:
    if col not in data.columns:
        raise ValueError(f"Missing required column: {col}")

# Convert date column to datetime format
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')  # Use errors='coerce' to handle invalid dates
if data['Date'].isnull().any():
    raise ValueError("There are invalid dates in the 'Date' column.")

# Sort the data by date
data = data.sort_values('Date')

# Calculate moving averages (7 days and 30 days)
data['MA_7'] = data['Close'].rolling(window=7).mean()
data['MA_30'] = data['Close'].rolling(window=30).mean()

# Calculate RSI
delta = data['Close'].diff()
gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
rs = gain / loss
data['RSI'] = 100 - (100 / (1 + rs))

# Calculate MACD
data['EMA_12'] = data['Close'].ewm(span=12, adjust=False).mean()
data['EMA_26'] = data['Close'].ewm(span=26, adjust=False).mean()
data['MACD'] = data['EMA_12'] - data['EMA_26']

# Drop rows with NaN values generated from moving averages or RSI calculations
data.dropna(inplace=True)

# Save the processed data
output_file = 'data/processed_data.csv'
data.to_csv(output_file, index=False)

print(f"Preprocessing completed and saved to '{output_file}'.")
