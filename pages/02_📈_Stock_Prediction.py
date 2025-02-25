# Imports
import plotly.graph_objects as go
import streamlit as st

# Import helper functions
from helper import *



# Configure the page for full width
st.set_page_config(
    page_title="Stock Price Prediction",
    page_icon="📈",
    layout="wide",  # Set layout to wide for full-width coverage
)

# Custom CSS for enhanced aesthetics and full-width layout
st.markdown(
    """
    <style>
    .main {
        max-width: 100% !important;
        padding: 2rem;
        background-color: #f9f9f9;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    h1 {
        color: #2c3e50;
        font-family: 'Georgia', serif;
        text-align: center;
    }
    h2 {
        color: #34495e;
        font-family: 'Arial', sans-serif;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }
    h3 {
        color: #34495e;
        font-family: 'Arial', sans-serif;
    }
    p {
        color: #666;
        font-family: 'Verdana', sans-serif;
        line-height: 1.6;
    }
    .footer {
        text-align: center;
        color: #777;
        padding: 1rem;
        margin-top: 2rem;
        border-top: 1px solid #ddd;
    }
    .stButton button {
        width: 100%;
        background-color: #3498db;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
    .stButton button:hover {
        background-color: #2980b9;
    }
    .stSelectbox, .stRadio {
        margin-bottom: 1rem;
    }
    .stTextInput {
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

##### Sidebar Start #####

# Add a sidebar
st.sidebar.markdown("## **User Input Features**")

# Fetch and store the stock data
stock_dict = fetch_stocks()

# Add a dropdown for selecting the stock
st.sidebar.markdown("### **Select stock**")
stock = st.sidebar.selectbox("Choose a stock", list(stock_dict.keys()))

# Add a selector for stock exchange
st.sidebar.markdown("### **Select stock exchange**")
stock_exchange = st.sidebar.radio("Choose a stock exchange", ("BSE", "NSE"), index=1)

# Build the stock ticker
stock_ticker = f"{stock_dict[stock]}.{'BO' if stock_exchange == 'BSE' else 'NS'}"

# Add a disabled input for stock ticker
st.sidebar.markdown("### **Stock ticker**")
st.sidebar.text_input(
    label="Stock ticker code", placeholder=stock_ticker, disabled=True
)

# Fetch and store periods and intervals
periods = fetch_periods_intervals()

# Add a selector for period
st.sidebar.markdown("### **Select period**")
period = st.sidebar.selectbox("Choose a period", list(periods.keys()))

# Add a selector for interval
st.sidebar.markdown("### **Select interval**")
interval = st.sidebar.selectbox("Choose an interval", periods[period])

##### Sidebar End #####


##### Title #####

# Add title to the app
st.markdown("# **Stock Price Prediction**")

# Add a subtitle to the app
st.markdown("##### **Enhance Investment Decisions through Data-Driven Forecasting**")

##### Title End #####


# Fetch the stock historical data
stock_data = fetch_stock_history(stock_ticker, period, interval)


##### Historical Data Graph #####

# Add a title to the historical data graph
st.markdown("## **Historical Data**")

# Create a plot for the historical data
fig = go.Figure(
    data=[
        go.Candlestick(
            x=stock_data.index,
            open=stock_data["Open"],
            high=stock_data["High"],
            low=stock_data["Low"],
            close=stock_data["Close"],
        )
    ]
)

# Customize the historical data graph
fig.update_layout(xaxis_rangeslider_visible=True)

# Use the native streamlit theme.
st.plotly_chart(fig, use_container_width=True)

##### Historical Data Graph End #####


##### Stock Prediction Graph #####

# Unpack the data
train_df, test_df, forecast, predictions, r2, MAPE = generate_stock_prediction(stock_ticker)

# Check if the data is not None
if train_df is not None and (forecast >= 0).all() and (predictions >= 0).all():
    # Add a title to the stock prediction graph
    st.markdown("## **Stock Prediction**")

    # Create a plot for the stock prediction
    fig = go.Figure(
        data=[
            go.Scatter(
                x=train_df.index,
                y=train_df["Close"],
                name="Train",
                mode="lines",
                line=dict(color="blue"),
            ),
            go.Scatter(
                x=test_df.index,
                y=test_df["Close"],
                name="Test",
                mode="lines",
                line=dict(color="orange"),
            ),
            go.Scatter(
                x=forecast.index,
                y=forecast,
                name="Forecast",
                mode="lines",
                line=dict(color="red"),
            ),
            go.Scatter(
                x=test_df.index,
                y=predictions,
                name="Test Predictions",
                mode="lines",
                line=dict(color="green"),
            ),
        ]
    )

    # Customize the stock prediction graph
    fig.update_layout(xaxis_rangeslider_visible=True)

    # Use the native streamlit theme.
    st.plotly_chart(fig, use_container_width=True)

# If the data is None
else:
    # Add a title to the stock prediction graph
    st.markdown("## **Stock Prediction**")

    # Add a message to the stock prediction graph
    st.markdown("### **No data available for the selected stock**")

##### Stock Prediction Graph End #####


##### Accuracy Measure Section #####

# Display a markdown header for the accuracy measure section
st.markdown("#### Accuracy Measure Between Test and Prediction")

# Create two columns for displaying R2 and MAPE
col1, col2 = st.columns(2)

# Display R2 in the first column with larger font size
with col1:
    st.subheader("R² Score")
    st.markdown(f"<h3 style='font-size:24px;'>{r2:.2f}</h3>", unsafe_allow_html=True)

# Display MAPE in the second column with larger font size
with col2:
    st.subheader("Mean Absolute Percentage Error (MAPE:.2f)")
    st.markdown(f"<h3 style='font-size:24px;'>{MAPE}</h3>", unsafe_allow_html=True)

##### Accuracy Measure Section End #####


##### Footer #####

# Footer
st.markdown("---")
st.markdown(
    """
    <div class="footer">
        <p>💼 Powered by Advanced Financial Analytics</p>
        <p style='font-size: 0.8em;'>Data sourced from Yahoo Finance</p>
    </div>
    """,
    unsafe_allow_html=True,
)

##### Footer End #####
