# Import streamlit
import streamlit as st

# Import helper functions
from helper import *

# Configure the page for full width
st.set_page_config(
    page_title="Stock Info",
    page_icon="🏛️",
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
    .dataframe {
        width: 100% !important;
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
default_stock_ticker = f"{stock_dict[stock]}.{'BO' if stock_exchange == 'BSE' else 'NS'}"

# Add a disabled input for stock ticker
st.sidebar.markdown("### **Stock ticker**")
user_stock_ticker = st.sidebar.text_input(
    label="Stock ticker code", value=default_stock_ticker, placeholder="Enter stock ticker"
)

# Final ticker selection logic: User input takes precedence if modified
stock_ticker = user_stock_ticker if user_stock_ticker else default_stock_ticker
# Display the selected ticker
st.sidebar.write(f"Selected Stock Ticker: {stock_ticker}")

##### Sidebar End #####


# Fetch the info of the stock
try:
    stock_data_info = fetch_stock_info(stock_ticker)
except:
    st.error("Error: Unable to fetch the stock data. Please try again later.")
    st.stop()


##### Title #####

# Add title to the app
st.markdown("# **Stock Info Plus**")

# Add a subtitle to the app
st.markdown("##### **Enhancing Your Stock Market Insights**")

##### Title End #####


##### Basic Information #####

# Add a heading
st.markdown("## **Basic Information**")

# Create 2 columns
col1, col2 = st.columns(2)

# Row 1
col1.dataframe(
    pd.DataFrame({"Issuer Name": [stock_data_info["Basic Information"]["longName"]]}),
    hide_index=True,
)
col2.dataframe(
    pd.DataFrame({"Symbol": [stock_ticker]}),
    hide_index=True,
)

# Row 2
col1.dataframe(
    pd.DataFrame({"Currency": [stock_data_info["Basic Information"]["currency"]]}),
    hide_index=True,
)
col2.dataframe(pd.DataFrame({"Exchange": [stock_exchange]}), hide_index=True)

##### Basic Information End #####


##### Market Data #####

# Add a heading
st.markdown("## **Market Data**")

# Create 2 columns
col1, col2 = st.columns(2)

# Row 1
col1.dataframe(
    pd.DataFrame({"Current Price": [stock_data_info["Market Data"]["currentPrice"]]}),
    hide_index=True,
)
col2.dataframe(
    pd.DataFrame({"Previous Close": [stock_data_info["Market Data"]["previousClose"]]}),
    hide_index=True,
)

# Create 3 columns
col1, col2, col3 = st.columns(3)

# Row 1
col1.dataframe(
    pd.DataFrame({"Open": [stock_data_info["Market Data"]["open"]]}),
    hide_index=True,
)
col2.dataframe(
    pd.DataFrame({"Day Low": [stock_data_info["Market Data"]["dayLow"]]}),
    hide_index=True,
)
col3.dataframe(
    pd.DataFrame({"Day High": [stock_data_info["Market Data"]["dayHigh"]]}),
    hide_index=True,
)

# Create 2 columns
col1, col2 = st.columns(2)

# Row 1
col1.dataframe(
    pd.DataFrame(
        {
            "Regular Market Previous Close": [
                stock_data_info["Market Data"]["regularMarketPreviousClose"]
            ]
        }
    ),
    hide_index=True,
)
col2.dataframe(
    pd.DataFrame(
        {"Regular Market Open": [stock_data_info["Market Data"]["regularMarketOpen"]]}
    ),
    hide_index=True,
)

# Row 2
col1.dataframe(
    pd.DataFrame(
        {
            "Regular Market Day Low": [
                stock_data_info["Market Data"]["regularMarketDayLow"]
            ]
        }
    ),
    hide_index=True,
)
col2.dataframe(
    pd.DataFrame(
        {
            "Regular Market Day High": [
                stock_data_info["Market Data"]["regularMarketDayHigh"]
            ]
        }
    ),
    hide_index=True,
)

# Create 3 columns
col1, col2, col3 = st.columns(3)

# Row 1
col1.dataframe(
    pd.DataFrame(
        {"Fifty-Two Week Low": [stock_data_info["Market Data"]["fiftyTwoWeekLow"]]}
    ),
    hide_index=True,
)
col2.dataframe(
    pd.DataFrame(
        {"Fifty-Two Week High": [stock_data_info["Market Data"]["fiftyTwoWeekHigh"]]}
    ),
    hide_index=True,
)
col3.dataframe(
    pd.DataFrame(
        {"Fifty-Day Average": [stock_data_info["Market Data"]["fiftyDayAverage"]]}
    ),
    hide_index=True,
)

##### Market Data End #####


##### Volume and Shares #####

# Add a heading
st.markdown("## **Volume and Shares**")

# Create 2 columns
col1, col2 = st.columns(2)

col1.dataframe(
    pd.DataFrame({"Volume": [stock_data_info["Volume and Shares"]["volume"]]}),
    hide_index=True,
)
col2.dataframe(
    pd.DataFrame(
        {
            "Regular Market Volume": [
                stock_data_info["Volume and Shares"]["regularMarketVolume"]
            ]
        }
    ),
    hide_index=True,
)

# Create 3 columns
col1, col2, col3 = st.columns(3)

# Row 1
col1.dataframe(
    pd.DataFrame(
        {"Average Volume": [stock_data_info["Volume and Shares"]["averageVolume"]]}
    ),
    hide_index=True,
)
col2.dataframe(
    pd.DataFrame(
        {
            "Average Volume (10 Days)": [
                stock_data_info["Volume and Shares"]["averageVolume10days"]
            ]
        }
    ),
    hide_index=True,
)
col3.dataframe(
    pd.DataFrame(
        {
            "Average Daily Volume (10 Day)": [
                stock_data_info["Volume and Shares"]["averageDailyVolume10Day"]
            ]
        }
    ),
    hide_index=True,
)

# Row 2
col1.dataframe(
    pd.DataFrame(
        {
            "Shares Outstanding": [
                stock_data_info["Volume and Shares"]["sharesOutstanding"]
            ]
        }
    ),
    hide_index=True,
)
col2.dataframe(
    pd.DataFrame(
        {
            "Implied Shares Outstanding": [
                stock_data_info["Volume and Shares"]["impliedSharesOutstanding"]
            ]
        }
    ),
    hide_index=True,
)
col3.dataframe(
    pd.DataFrame(
        {"Float Shares": [stock_data_info["Volume and Shares"]["floatShares"]]}
    ),
    hide_index=True,
)

##### Volume and Shares End #####


##### Dividends and Yield #####

# Add a heading
st.markdown("## **Dividends and Yield**")

# Create 3 columns
col1, col2, col3 = st.columns(3)

# Row 1
col1.dataframe(
    pd.DataFrame(
        {"Dividend Rate": [stock_data_info["Dividends and Yield"]["dividendRate"]]}
    ),
    hide_index=True,
)
col2.dataframe(
    pd.DataFrame(
        {"Dividend Yield": [stock_data_info["Dividends and Yield"]["dividendYield"]]}
    ),
    hide_index=True,
)
col3.dataframe(
    pd.DataFrame(
        {"Payout Ratio": [stock_data_info["Dividends and Yield"]["payoutRatio"]]}
    ),
    hide_index=True,
)

##### Dividends and Yield End #####


##### Valuation and Ratios #####

# Add a heading
st.markdown("## **Valuation and Ratios**")

# Create 2 columns
col1, col2 = st.columns(2)

# Row 1
col1.dataframe(
    pd.DataFrame(
        {"Market Cap": [stock_data_info["Valuation and Ratios"]["marketCap"]]}
    ),
    hide_index=True,
)
col2.dataframe(
    pd.DataFrame(
        {
            "Enterprise Value": [
                stock_data_info["Valuation and Ratios"]["enterpriseValue"]
            ]
        }
    ),
    hide_index=True,
)

# Row 2
col1.dataframe(
    pd.DataFrame(
        {"Price to Book": [stock_data_info["Valuation and Ratios"]["priceToBook"]]}
    ),
    hide_index=True,
)
col2.dataframe(
    pd.DataFrame(
        {"Debt to Equity": [stock_data_info["Valuation and Ratios"]["debtToEquity"]]}
    ),
    hide_index=True,
)

# Row 3
col1.dataframe(
    pd.DataFrame(
        {"Gross Margins": [stock_data_info["Valuation and Ratios"]["grossMargins"]]}
    ),
    hide_index=True,
)
col2.dataframe(
    pd.DataFrame(
        {"Profit Margins": [stock_data_info["Valuation and Ratios"]["profitMargins"]]}
    ),
    hide_index=True,
)

##### Valuation and Ratios End #####


##### Financial Performance #####

# Add a heading
st.markdown("## **Financial Performance**")

# Create 2 columns
col1, col2 = st.columns(2)

# Row 1
col1.dataframe(
    pd.DataFrame(
        {"Total Revenue": [stock_data_info["Financial Performance"]["totalRevenue"]]}
    ),
    hide_index=True,
)
col2.dataframe(
    pd.DataFrame(
        {
            "Revenue Per Share": [
                stock_data_info["Financial Performance"]["revenuePerShare"]
            ]
        }
    ),
    hide_index=True,
)

# Create 3 columns
col1, col2, col3 = st.columns(3)

# Row 1
col1.dataframe(
    pd.DataFrame(
        {"Total Cash": [stock_data_info["Financial Performance"]["totalCash"]]}
    ),
    hide_index=True,
)
col2.dataframe(
    pd.DataFrame(
        {
            "Total Cash Per Share": [
                stock_data_info["Financial Performance"]["totalCashPerShare"]
            ]
        }
    ),
    hide_index=True,
)
col3.dataframe(
    pd.DataFrame(
        {"Total Debt": [stock_data_info["Financial Performance"]["totalDebt"]]}
    ),
    hide_index=True,
)

# Create 2 columns
col1, col2 = st.columns(2)

# Row 1
col1.dataframe(
    pd.DataFrame(
        {
            "Earnings Growth": [
                stock_data_info["Financial Performance"]["earningsGrowth"]
            ]
        }
    ),
    hide_index=True,
)
col2.dataframe(
    pd.DataFrame(
        {"Revenue Growth": [stock_data_info["Financial Performance"]["revenueGrowth"]]}
    ),
    hide_index=True,
)

# Row 2
col1.dataframe(
    pd.DataFrame(
        {
            "Return on Assets": [
                stock_data_info["Financial Performance"]["returnOnAssets"]
            ]
        }
    ),
    hide_index=True,
)
col2.dataframe(
    pd.DataFrame(
        {
            "Return on Equity": [
                stock_data_info["Financial Performance"]["returnOnEquity"]
            ]
        }
    ),
    hide_index=True,
)

##### Financial Performance End #####


##### Cash Flow #####

# Add a heading
st.markdown("## **Cash Flow**")

# Create 2 columns
col1, col2 = st.columns(2)

# Row 2
col1.dataframe(
    pd.DataFrame({"Free Cash Flow": [stock_data_info["Cash Flow"]["freeCashflow"]]}),
    hide_index=True,
)
col2.dataframe(
    pd.DataFrame(
        {"Operating Cash Flow": [stock_data_info["Cash Flow"]["operatingCashflow"]]}
    ),
    hide_index=True,
)

##### Cash Flow End #####


##### Analyst Targets #####

# Add a heading
st.markdown("## **Analyst Targets**")

# Create 2 columns
col1, col2 = st.columns(2)

# Row 1
col1.dataframe(
    pd.DataFrame(
        {"Target High Price": [stock_data_info["Analyst Targets"]["targetHighPrice"]]}
    ),
    hide_index=True,
)
col2.dataframe(
    pd.DataFrame(
        {"Target Low Price": [stock_data_info["Analyst Targets"]["targetLowPrice"]]}
    ),
    hide_index=True,
)

# Row 2
col1.dataframe(
    pd.DataFrame(
        {"Target Mean Price": [stock_data_info["Analyst Targets"]["targetMeanPrice"]]}
    ),
    hide_index=True,
)
col2.dataframe(
    pd.DataFrame(
        {
            "Target Median Price": [
                stock_data_info["Analyst Targets"]["targetMedianPrice"]
            ]
        }
    ),
    hide_index=True,
)

##### Analyst Targets End #####


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