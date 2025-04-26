import streamlit as st
from data import AirtableManager

# Initialize Airtable
airtable = AirtableManager()

def main():
    st.title("Stock Price Predictions")
    
    # Get prediction data from Airtable
    predicted_data = airtable.retrieve_data()
    
    if predicted_data is not None:
        st.header("Current Predictions")
        
        # Display the data in a simple table
        st.dataframe(
            predicted_data,
            column_config={
                "Ticker": "Stock Ticker",
                "Predicted Price": st.column_config.NumberColumn(
                    "Predicted Price (₹)",
                    format="₹%.2f"
                )
            },
            hide_index=True,
            use_container_width=True
        )
        
    else:
        st.warning("No prediction data available. Please run main.py first.")

if __name__ == "__main__":
    main()