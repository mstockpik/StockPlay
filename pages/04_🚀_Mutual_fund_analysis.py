import pandas as pd
import urllib.request, json
import plotly_express as px
import plotly.figure_factory as ff
import streamlit as st
import numpy as np
from pyxirr import xirr
import datetime

# Page Configuration
st.set_page_config(
    page_title="Mutual Fund Analytics Dashboard 📈",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main-header {
        font-size: 34px;
        color: #1E3D59;
        text-align: center;
        padding: 20px;
        background: linear-gradient(to right, #E8F1F5, #B3E0F2);
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: #F0F8FF;
        padding: 10px;
        border-radius: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        background-color: white;
        border-radius: 5px;
        color: #1E3D59;
        font-weight: 500;
    }
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .sidebar-info {
        padding: 15px;
        background-color: #F0F8FF;
        border-radius: 5px;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🚀 Mutual Fund Analytics Dashboard</div>', unsafe_allow_html=True)

# Cached Functions
@st.cache_data(ttl=3600)
def get_scheme_codes():
    try:
        with open('./data/mf_codes.txt', 'r') as fp:
            list_code = []
            line = fp.readline()
            while line:
                words = line.strip().split(';')
                if len(words) > 5:
                    list_code.append([words[i] for i in [0, 1, 3]])
                line = fp.readline()
        df_codes = pd.DataFrame(list_code)
        df_codes.columns = ['schemeCode', 'schemeISIN', 'schemeName']
        return df_codes
    except Exception as e:
        st.error(f"Error loading scheme codes: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def get_nav(scheme_code='122639'):
    try:
        with st.spinner('Fetching NAV data...'):
            mf_url = f'https://api.mfapi.in/mf/{scheme_code}'
            with urllib.request.urlopen(mf_url) as url:
                data = json.load(url)
            df_navs = pd.DataFrame(data['data'])
            df_navs['date'] = pd.to_datetime(df_navs.date, format='%d-%m-%Y')
            df_navs['nav'] = df_navs['nav'].astype(float)
            df_navs = df_navs.sort_values(['date']).set_index(['date'])
            df_dates = pd.DataFrame(
                pd.date_range(start=df_navs.index.min(), end=df_navs.index.max()),
                columns=['date']
            ).set_index(['date'])
            df_navs = df_navs.join(df_dates, how='outer').ffill().reset_index()
            return df_navs
    except Exception as e:
        st.error(f"Error fetching NAV data: {str(e)}")
        return pd.DataFrame()

@st.cache_data
def get_cagr(df_navs_orig, num_years=1):
    df_navs = df_navs_orig.copy()
    df_navs['prev_nav'] = df_navs.nav.shift(365 * num_years)
    df_navs = df_navs.dropna()
    df_navs['returns'] = df_navs['nav'] / df_navs['prev_nav'] - 1
    df_navs['cagr'] = 100 * ((1 + df_navs['returns']) ** (1 / num_years) - 1)
    df_navs['years'] = num_years
    return df_navs[['date', 'years', 'cagr']]
	
# Sidebar Configuration
st.sidebar.markdown('<h2 style="text-align: center;">🔍 Fund Selection</h2>', unsafe_allow_html=True)


# Load Data 
df_mfs = get_scheme_codes()
scheme_names = sorted(df_mfs.schemeName.unique().tolist())

# Set default value
default_selection = [scheme_names[0]] if scheme_names else []

# Enhanced Fund Selection
sel_names = st.sidebar.multiselect(
    "Select a Mutual Fund:",
    scheme_names,
    default=default_selection,
    max_selections=1,
    help="Choose a mutual fund to analyze"
)


# Informative Sidebar
st.sidebar.markdown("""
    <div class="sidebar-info">
    💡 <b>Quick Guide:</b>
    <ul>
        <li>📊 View historical NAV trends</li>
        <li>📈 Analyze CAGR performance</li>
        <li>🔄 Compare with other funds</li>
        <li>💰 Calculate SIP returns</li>
    </ul>
    </div>
""", unsafe_allow_html=True)

if not sel_names:
    st.info("👈 Please select a mutual fund from the sidebar to begin analysis")
    st.stop()

sel_name = sel_names[0]
st.markdown(f"### Selected Fund: {sel_name} 📊")

# Enhanced Tabs
tab_nav, tab_cagr, tab_comp, tab_sip = st.tabs([
    "📈 NAV History",
    "📊 CAGR Analysis", 
    "🔄 Comparative Analysis",
    "💰 SIP Calculator"
])

# Get Fund Data
sel_code = df_mfs[df_mfs['schemeName'] == sel_name].schemeCode.to_list()[0]
df_navs = get_nav(str(sel_code))

# NAV History Tab
with tab_nav:
    st.subheader("📈 NAV History Analysis")
    
    # Enhanced NAV Chart
    fig1 = px.line(df_navs, x='date', y='nav', log_y=True)
    fig1.update_layout(
        title=f"NAV Trend: {sel_name}",
        xaxis_title="Date",
        yaxis_title="NAV (Log Scale)",
        template="plotly_white",
        hovermode='x unified'
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # Key Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current NAV", f"₹{df_navs.iloc[-1]['nav']:.2f}", 
                 f"{((df_navs.iloc[-1]['nav']/df_navs.iloc[-2]['nav'])-1)*100:.2f}%")
    with col2:
        st.metric("Highest NAV", f"₹{df_navs['nav'].max():.2f}")
    with col3:
        st.metric("Lowest NAV", f"₹{df_navs['nav'].min():.2f}")

# CAGR Analysis Tab
with tab_cagr:
    st.subheader("📊 CAGR Analysis")
    
    years = list(range(1, 11))
    list_cagr = [get_cagr(df_navs, y) for y in years]
    df_cagrs = pd.concat(list_cagr)
    
    # Enhanced CAGR Chart
    fig2 = px.line(df_cagrs, x='date', y='cagr', color='years',
                   title="CAGR Trends Over Different Time Periods")
    fig2.update_layout(
        xaxis_title="Date",
        yaxis_title="CAGR (%)",
        template="plotly_white",
        hovermode='x unified'
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    # CAGR Statistics
    dfx = df_cagrs[['years', 'cagr']].groupby('years').describe().reset_index()
    dfx.columns = [[a for (a, b) in dfx.columns][0]] + [a for a in dfx.columns.droplevel()][1:]
    
    st.markdown("### 📊 CAGR Statistics")
    st.dataframe(dfx.style.format({
        'mean': '{:.2f}%',
        'std': '{:.2f}%',
        'min': '{:.2f}%',
        '25%': '{:.2f}%',
        '50%': '{:.2f}%',
        '75%': '{:.2f}%',
        'max': '{:.2f}%'
    }))

# Comparative Analysis Tab
with tab_comp:
    st.subheader("🔄 Comparative Analysis")
    
    # Enhanced Fund Comparison Interface
    check_combo = st.checkbox("🔄 Compare with Fund Combination", value=False)
    names_comp = st.multiselect(
        "Select Funds for Comparison:",
        df_mfs.schemeName.unique(),
        max_selections=5,
        help="Choose up to 5 funds to compare"
    )
    
    all_names = [sel_name] + names_comp
    codes_comp = [df_mfs[df_mfs['schemeName'] == x].schemeCode.to_list()[0] for x in all_names]

    list_navs = []
    list_cagrs = []
    for name in all_names:
        code = df_mfs[df_mfs['schemeName'] == name].schemeCode.to_list()[0]
        df_nav_comp = get_nav(str(code))
        years = [x for x in range(1, 11)]
        list_cagr = []
        for y in years:
            df_cagr = get_cagr(df_nav_comp, y)
            list_cagr.append(df_cagr)
        df_cagrs_comp = pd.concat(list_cagr)

        df_nav_comp = df_nav_comp.set_index('date')
        df_nav_comp = df_nav_comp.rename(columns={'nav': name})
        list_navs.append(df_nav_comp)

        df_cagrs_comp = df_cagrs_comp.set_index(['date', 'years'])
        df_cagrs_comp = df_cagrs_comp.rename(columns={'cagr': name})
        list_cagrs.append(df_cagrs_comp)

    df_nav_all = pd.concat(list_navs, axis=1).dropna()

    if check_combo:
        if len(names_comp) == 0:
            wt = "100.0"
        else:
            wt = ((str(round(100 / len(names_comp), 2)) + ", ") * len(names_comp)).rstrip(", ")
        wt_text = st.text_input("Weightage:", value=wt)
        wt_nums = [float(x.strip()) for x in wt_text.split(",")]

        if sum(wt_nums) != 100.0:
            st.error("Weights do not add up to 100.0. Please Check!")
        else:
            st.write("Weights add up to 100.0.  Okay!")

        ctr = 0
        for name in names_comp:
            df_nav_all[name + '_wt'] = df_nav_all[name] * wt_nums[ctr] / 100
            ctr += 1
        names_wt = [name + '_wt' for name in names_comp]
        df_nav_all['combo'] = df_nav_all[names_wt].sum(axis=1)

        df_nav = df_nav_all.reset_index()[['date', 'combo']]
        df_nav.columns = ['date', 'nav']
        list_cagr = []
        for y in years:
            df_cagr = get_cagr(df_nav, y)
            list_cagr.append(df_cagr)
        df_cagrs_comp = pd.concat(list_cagr)
        df_cagrs_comp = df_cagrs_comp.set_index(['date', 'years'])
        df_cagrs_comp = df_cagrs_comp.rename(columns={'cagr': 'combo'})
        list_cagrs.append(df_cagrs_comp)
        all_names = all_names + ['combo']

    df_cagr_all = pd.concat(list_cagrs, axis=1).dropna()

    df_navs_date = df_nav_all.reset_index()
    min_date = df_navs_date['date'].min()
    max_date = df_navs_date['date'].max()
    st.write('Cumulative Returns Comparisons')
    from_date = st.date_input('From Date:', value=min_date, min_value=min_date, max_value=max_date)
    df_nav_all = df_navs_date[df_navs_date['date'] >= np.datetime64(from_date)].set_index('date')

    df_rebased = df_nav_all.div(df_nav_all.iloc[0]).reset_index()
    df_rebased_long = pd.melt(df_rebased, id_vars='date', value_vars=all_names, var_name='mf', value_name='nav')

    fig3 = px.line(df_rebased_long, x='date', y='nav', log_y=True, color='mf')
    fig3.update_layout(legend=dict(yanchor="bottom", y=-0.7, xanchor="left", x=0))
    st.plotly_chart(fig3)

    df_cagr_wide = df_cagr_all.reset_index()
    df_cagr_long = pd.melt(df_cagr_wide, id_vars=['date', 'years'], value_vars=all_names, var_name='mf', value_name='cagr')

    st.write("Rolling CAGR Comparison")
    sel_year = st.number_input('Investment Duration (Number of Years):', value=1, min_value=1, max_value=10, step=1)
    df_cagr_plot = df_cagr_long[df_cagr_long['years'] == sel_year]
    fig4 = px.line(df_cagr_plot, x='date', y='cagr', color='mf')
    fig4.update_layout(legend=dict(yanchor="bottom", y=-0.7, xanchor="left", x=0))
    st.plotly_chart(fig4)

    st.write('Draw Down Comparison')
    df_rebased_long['cum_max'] = df_rebased_long.groupby('mf').nav.cummax()
    df_rebased_long['draw_down'] = (df_rebased_long['nav'] - df_rebased_long['cum_max']) / df_rebased_long['cum_max']
    fig5 = px.line(df_rebased_long, x="date", y="draw_down", color="mf")
    fig5.update_layout(legend=dict(yanchor="bottom", y=-0.7, xanchor="left", x=0))
    st.plotly_chart(fig5)





# SIP Calculator Tab
with tab_sip:
    st.subheader("💰 SIP Calculator")
    
    # Enhanced Date Selection
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input('Start Date 📅', datetime.date(2006, 5, 1))
    with col2:
        end_date = st.date_input('End Date 📅', datetime.date(2024, 12, 31))

    df_dates = pd.DataFrame(pd.date_range(start=start_date, end=end_date, freq='ME'))
    df_dates.columns = ['date']

    df_cf = df_navs.merge(df_dates, on='date')
    df_cf['amount'] = 1000
    df_cf['units'] = df_cf['amount'] / df_cf['nav']
    df_cf['cum_units'] = df_cf['units'].cumsum()
    df_cf['cur_value'] = df_cf['cum_units'] * df_cf['nav']
    df_cf['inv_amount'] = df_cf['amount'].cumsum()
    df_cf = df_cf.reset_index()
    df_cf['amount'] = df_cf['amount'] * (1.05)**(df_cf['index'] // 12)

    df_investment = df_cf[['date', 'amount']]
    df_redemption = pd.DataFrame(
        [{'date': df_cf.iloc[-1:].date.values[0],
          'amount': -df_cf['units'].sum() * df_cf.iloc[-1:].nav.values[0]}])
    df_irr = pd.concat([df_investment, df_redemption]).reset_index(drop=True)

    xirr_value = xirr(df_irr[['date', 'amount']]) * 100
    st.write("XIRR: (%)")
    st.write(round(xirr_value,2))

    st.write('Invested Amount vs Current Value')
    df_daily_dates = pd.DataFrame(
        pd.date_range(start=df_cf['date'].min(), end=df_cf['date'].max(), freq='D'))
    df_daily_dates.columns = ['date']
    df_daily_navs = df_navs.merge(df_daily_dates, on='date')
    del df_cf['nav']
    df_cfs = df_cf.merge(df_daily_navs, on='date', how='right').sort_values(['date'])
    df_cfs = df_cfs.ffill()
    df_cfs['cur_value'] = df_cfs['cum_units'] * df_cfs['nav']
    df_cf_long = pd.melt(df_cfs[['date', 'inv_amount', 'cur_value']], id_vars=['date'],
                         value_vars=['inv_amount', 'cur_value'], var_name='component', value_name='amount')
    df_cf_long.loc[df_cf_long['component'] == 'inv_amount', 'component'] = 'Invested Amount'
    df_cf_long.loc[df_cf_long['component'] == 'cur_value', 'component'] = 'Current Value'
    fig6 = px.line(df_cf_long, x='date', y='amount', color='component')
    st.plotly_chart(fig6)

    st.write('Unit Accumulation - Normalized')
    df_cfs['cum_units'] = (df_cfs['cum_units'] / df_cfs.iloc[-1:].cum_units.values[0])
    df_cfs['inv_amount'] = (df_cfs['inv_amount'] / df_cfs.iloc[-1:].inv_amount.values[0])
    df_cf_long1 = pd.melt(df_cfs[['date', 'inv_amount', 'cum_units']], id_vars=['date'],
                         value_vars=['inv_amount', 'cum_units'], var_name='component', value_name='proportion')
    df_cf_long1.loc[df_cf_long1['component'] == 'inv_amount', 'component'] = 'Invested Amount'
    df_cf_long1.loc[df_cf_long1['component'] == 'cum_units', 'component'] = 'Accumulated Units'
    fig7 = px.line(df_cf_long1, x='date', y='proportion', color='component')
    # fig7 = px.line(df_cfs, x='date', y='cum_units')
    st.plotly_chart(fig7)



##### Footer #####

# Footer
st.markdown("---")
st.markdown(
    """
    <div class="footer"; div style='text-align: center; color: #666; padding: 20px;'>
        <p>💼 Powered by Advanced Financial Analytics</p>
        <p style='font-size: 0.8em;'>Data sourced from AMFI India</p>
    </div>
    """,
    unsafe_allow_html=True,
)

##### Footer End #####
