# Stock Price Prediction System

## Overview
This project is a stock price prediction system that uses LSTM neural networks to forecast next-day closing prices for selected Indian tech stocks. The system automatically updates predictions daily and stores them in Airtable, with a Streamlit web interface for displaying the results.

## Features
- **Automated daily predictions**: Runs predictions at midnight each day
- **LSTM model**: Uses historical price data with moving averages as features
- **Airtable integration**: Stores and retrieves prediction data
- **Streamlit dashboard**: Clean interface to view current predictions
- **Supported stocks**: TCS, Infosys, HCL Tech, Wipro, Tech Mahindra
