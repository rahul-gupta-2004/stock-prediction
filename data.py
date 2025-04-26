import os
import pandas as pd
from pyairtable import Api
from dotenv import load_dotenv
from datetime import datetime as dt

load_dotenv()

class AirtableManager:
    def __init__(self):
        self.api = Api(os.getenv('AIRTABLE_TOKEN'))
        self.base_id = os.getenv('AIRTABLE_BASE_ID')
        self.table_name = os.getenv('AIRTABLE_TABLE_NAME')
        self.table = self.api.table(self.base_id, self.table_name)
    
    def update_data(self, predicted_prices):
        """Store predicted prices in Airtable"""
        records = []
        for _, row in predicted_prices.iterrows():
            records.append({
                "ticker_name": row['Ticker'],
                "predicted_value": str(row['Predicted Price']),
            })
        
        # Clear existing records
        self.table.batch_delete([record['id'] for record in self.table.all()])
        # Add new records
        self.table.batch_create(records)
        print("Data updated in Airtable")

    def retrieve_data(self):
        """Retrieve predicted prices from Airtable"""
        records = self.table.all()
        if not records:
            print("No data found in Airtable")
            return None
        
        data = []
        for record in records:
            data.append({
                'Ticker': record['fields']['ticker_name'],
                'Predicted Price': float(record['fields']['predicted_value'])  # Convert back to float for calculations
            })
        
        return pd.DataFrame(data)