from data import AirtableManager
from predict_stock import predict_next_day
import pandas as pd
import datetime
import time

def train_and_update():
    tickers = ['TCS.NS', 'INFY.NS', 'HCLTECH.NS', 'WIPRO.NS', 'TECHM.NS']
    
    predicted_prices = pd.DataFrame(columns=['Ticker', 'Predicted Price'])
    
    for ticker in tickers:
        try:
            predicted_price = predict_next_day(ticker)
            new_row = pd.DataFrame({'Ticker': [ticker], 'Predicted Price': [predicted_price]})
            predicted_prices = pd.concat([predicted_prices, new_row], ignore_index=True).astype({'Predicted Price': 'float64'})
            print(f"Predicted next day price for {ticker}: {predicted_price:.2f}")
        except Exception as e:
            print(f"Error predicting for {ticker}: {str(e)}")
    
    # Update Airtable
    airtable = AirtableManager()
    airtable.update_data(predicted_prices)

def should_update():
    """Check if current time is between 12:00 AM and 12:05 AM"""
    now = datetime.datetime.now()
    return now.hour == 0 and now.minute < 5

if __name__ == "__main__":
    print("Running stock prediction scheduler...")
    while True:
        if should_update():
            print("Midnight update triggered...")
            train_and_update()
            print("Prediction completed and data updated in Airtable")
            # Sleep for 1 hour after update to prevent multiple runs
            time.sleep(3600)
        else:
            # Check every 5 minutes
            time.sleep(300)
        print(f"Next check at: {(datetime.datetime.now() + datetime.timedelta(minutes=5)).strftime('%H:%M')}")