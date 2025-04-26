from datetime import datetime
import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.callbacks import EarlyStopping

def fetch_stock_data(stock_symbol, start_date, end_date):
    """Fetch stock data from Yahoo Finance"""
    data = yf.download(stock_symbol, start=start_date, end=end_date, auto_adjust=True)
    return data

def preprocess_data(data, time_step=1, test_size=0.2):
    """Prepare data for LSTM model"""
    # Calculate moving averages
    data['SMA_10'] = data['Close'].rolling(window=10).mean()
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    data.dropna(inplace=True)
    
    # Scale features
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data[['Close', 'SMA_10', 'SMA_50', 'Volume']])
    
    # Create sequences for LSTM
    X, y = [], []
    for i in range(len(scaled_data) - time_step - 1):
        X.append(scaled_data[i:(i + time_step), :])  # All features
        y.append(scaled_data[i + time_step, 0])  # Only 'Close' price as target
    X, y = np.array(X), np.array(y)
    
    # Train-test split
    split = int(len(X) * (1 - test_size))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    
    return X_train, y_train, X_test, y_test, scaler

def build_lstm_model(input_shape):
    """Build LSTM model architecture"""
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def predict_next_day(ticker, time_steps=10):
    """Predict next day's closing price"""
    # Fetch data
    end_date = datetime.now().strftime('%Y-%m-%d')
    data = fetch_stock_data(ticker, '2010-01-01', end_date)
    
    # Preprocess data
    X_train, y_train, _, _, scaler = preprocess_data(data, time_step=time_steps)
    
    # Build and train model
    model = build_lstm_model((X_train.shape[1], X_train.shape[2]))
    early_stopping = EarlyStopping(monitor='loss', patience=5, restore_best_weights=True)
    model.fit(X_train, y_train, epochs=50, batch_size=32, 
              callbacks=[early_stopping], verbose=0)
    
    # Prepare last sequence for prediction
    last_sequence = scaler.transform(data[['Close', 'SMA_10', 'SMA_50', 'Volume']].tail(time_steps))
    last_sequence = np.reshape(last_sequence, (1, time_steps, last_sequence.shape[1]))
    
    # Make prediction
    predicted_scaled = model.predict(last_sequence)
    predicted_price = scaler.inverse_transform(
        np.concatenate([predicted_scaled, np.zeros((1, 3))], axis=1)
    )[0, 0]
    
    return predicted_price