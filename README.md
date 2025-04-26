# Stock Price Prediction System

## Overview
This project is a stock price prediction system that uses LSTM neural networks to forecast next-day closing prices for selected Indian tech stocks. The system automatically updates predictions daily and stores them in Airtable, with a Streamlit web interface for displaying the results.

## Features
- **Automated daily predictions**: Runs predictions at midnight each day
- **LSTM model**: Uses historical price data with moving averages as features
- **Airtable integration**: Stores and retrieves prediction data
- **Streamlit dashboard**: Clean interface to view current predictions
- **Supported stocks**: TCS, Infosys, HCL Tech, Wipro, Tech Mahindra

## How It Works
1. **Data Collection**: Fetches historical stock data from Yahoo Finance
2. **Preprocessing**: Calculates moving averages and scales features
3. **Model Training**: Uses Keras LSTM model with early stopping
4. **Prediction**: Forecasts next day's closing price
5. **Storage**: Updates Airtable with new predictions
6. **Visualization**: Streamlit app displays current predictions

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/stock-price-prediction.git
   cd stock-price-prediction
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Airtable credentials:
   ```
   AIRTABLE_TOKEN=your_api_token
   AIRTABLE_BASE_ID=your_base_id
   AIRTABLE_TABLE_NAME=your_table_name
   ```

## Usage
