# Bitcoin Price Prediction

This project is a web application that predicts Bitcoin prices for the next 10 days based on historical data. It utilizes a Flask backend for handling predictions and fetching data from the CoinGecko API, and a JavaScript frontend for displaying the results in a user-friendly manner.

## how to run this

## Activate virtual environment:

venv\Scripts\activate

## first run this

python scripts/preprocess.py

## second run this

python scripts/train_model.py

## next run this

python scripts/predict.py

## after these run this

python app.py

## Table of Contents

- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Technologies Used

- **Backend**:
  - Python
  - Flask
  - Pandas
  - NumPy
  - Requests
  - Logging
- **Frontend**:
  - HTML
  - CSS
  - JavaScript
  - Chart.js (for data visualization)

## Installation

Navigate to the project directory:

cd <project-directory>
Install required dependencies for the backend:

pip install -r requirements.txt
Start the Flask server:

python app.py
Open the index.html file in your browser to view the application.

Usage
When the application loads, it will automatically fetch and display predictions for the next 10 days, along with advice on whether to buy or sell based on the predicted trend.
The predictions will be shown in a line chart, and a table will display the predicted prices for each date.
API Endpoints
/predict
Method: GET
Description: Fetches predicted prices and related metrics.
Response:
json
Copy code
{
"current_price": "$XXX.XX USD",
"predictions": [
{
"Date": "YYYY-MM-DD",
"Predicted Price": number,
"Percentage Change (%)": number,
"Volatility": number
},
...
],
"advice": "Your advice message",
"absolute_mean": number,
"mae": number,
"mse": number,
"predicted_trend": "upward/downward",
"target_price": number,
"long_term_predictions": [
{
"Date": "YYYY-MM-DD",
"Predicted Price": number
},
...
],
"historical_prices": [
{
"Date": "YYYY-MM-DD",
"Actual Price": number
},
...
]
}
Features
Prediction Model: Generates short-term and long-term price predictions based on historical Bitcoin prices.
Data Visualization: Displays predicted prices in a responsive line chart using Chart.js.
Error Handling: Provides user-friendly error messages when fetching predictions fails.
Performance Metrics: Calculates and displays performance metrics like Mean Absolute Error (MAE) and Mean Squared Error (MSE).
Contributing
Fork the repository.

Create your feature branch:

git checkout -b feature/YourFeature
Commit your changes:

git commit -m 'Add some feature'
Push to the branch:

git push origin feature/YourFeature
Open a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details.

python
Copy code

### Instructions

- Replace `<repository-url>` with the URL of your GitHub repository.
- Replace `<project-directory>` with the actual name of your project directory.

Feel free to modify any section to better fit your project details! Let me know if you need any additional help or changes.

Backend (Python)
Flask: A lightweight WSGI web application framework for building the API.

Installation: flask
Pandas: A powerful data manipulation and analysis library, used for handling time series data.

Installation: pandas
NumPy: A library for numerical computations, often used for handling arrays and mathematical functions.

Installation: numpy
Requests: A simple HTTP library for Python to make API requests.

Installation: requests
Flask-CORS: A Flask extension for handling Cross-Origin Resource Sharing (CORS), allowing your API to be accessed from different origins.

Installation: flask-cors
Logging: Built-in Python module for logging messages.

No installation required.
Scikit-learn (if you're using machine learning models): A machine learning library for Python, often used for making predictions.

Installation: scikit-learn
Statsmodels (optional): A library for estimating and testing statistical models, if you're doing time series analysis.

Installation: statsmodels
Frontend (JavaScript/HTML/CSS)
Chart.js: A library for creating charts and visualizations in the frontend.
Installation: Include the script in your HTML:
html
Copy code

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

Example requirements.txt
You can create a requirements.txt file for your backend Python dependencies as follows:

Flask
pandas
numpy
requests
flask-cors
scikit-learn
statsmodels
Installation Command
To install all the packages listed in the requirements.txt, you can use the following command:

pip install -r requirements.txt
Note
Make sure to include only the modules you have used in your actual implementation. If you've added or removed any modules during development, adjust the list accordingly. Let me know if you need help with anything else!
