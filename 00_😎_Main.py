import streamlit as st

# Configure the page settings for full width
st.set_page_config(
    page_title="Stock Prediction App",
    page_icon="📊",
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
    </style>
    """,
    unsafe_allow_html=True,
)

# Main content
st.markdown(
    """
    # 📈 **StockPlay: Intelligent Stock Forecasting**
    ### **Empowering Investors with Machine Learning-Driven Insights**

    **StockPlay** is a cutting-edge stock price prediction application designed to assist investors in making informed, data-driven decisions. Leveraging advanced machine learning algorithms, StockPlay provides accurate forecasts and actionable insights into stock market trends.

    ## 🏗️ **Core Architecture**

    StockPlay is built using a robust stack of modern technologies and frameworks:

    - **Streamlit**: For creating an intuitive and interactive web interface.
    - **YFinance**: To seamlessly retrieve real-time financial data from Yahoo Finance.
    - **StatsModels**: For implementing the ARIMA time series forecasting model.
    - **Plotly**: To generate dynamic and interactive financial visualizations.

    ### **Workflow Overview**

    1. **Stock Selection**: Users input a stock ticker symbol.
    2. **Data Retrieval**: Historical stock data is fetched using the YFinance API.
    3. **Model Training**: The ARIMA model is trained on the historical data.
    4. **Price Forecasting**: The model generates multi-day price predictions.
    5. **Visualization**: Results are displayed through interactive charts using Plotly.

    ## 🎯 **Key Features**

    - **Real-Time Data Integration**: Access up-to-date stock prices and fundamental metrics.
    - **Interactive Financial Charts**: Explore historical trends and forecasted prices with ease.
    - **ARIMA Forecasting**: Benefit from statistically robust and reliable predictions.
    - **Backtesting Capabilities**: Evaluate model accuracy with historical data.
    - **Responsive Design**: Enjoy a seamless experience across all devices.

    ## 🚀 **Future Enhancements**

    StockPlay is continuously evolving. Here’s a glimpse of what’s on the horizon:

    - **Advanced Forecasting Models**: Integration of LSTM and other deep learning techniques.
    - **Quantitative Trading Strategies**: Automated trading strategies based on predictive analytics.
    - **Portfolio Optimization**: Tools for building and tracking optimized investment portfolios.
    - **Expanded Fundamental Data**: Inclusion of additional financial metrics and indicators.
    - **User Account System**: Personalized dashboards and saved preferences for registered users.

    """,
    unsafe_allow_html=True,
)

# Footer
st.markdown("---")
st.markdown(
    """
    <div class="footer">
        <p>⚖️ **Disclaimer**</p>
        <p>This application is for informational purposes only and does not constitute financial advice. Use the forecasted data to complement your own research and analysis. No guarantees are made regarding trading performance.</p>
        <p>💼 Powered by Advanced Financial Analytics</p>
    </div>
    """,
    unsafe_allow_html=True,
)