import streamlit as st
import pandas as pd
from newsapi import NewsApiClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize NewsAPI (Replace 'YOUR_API_KEY' with your actual API key)
newsapi = NewsApiClient(api_key='868d82c67ccf4bb586a4ced2c1a0f258')

# Streamlit App Title
st.set_page_config(page_title="News Sentiment Analyzer", layout="wide")
st.title("📰 News Sentiment Analyzer")
st.markdown("Analyze real-time news sentiment for any **stock ticker** or **company**.")

# Input field for user to enter a stock ticker or company name
ticker = st.text_input("Enter a Stock Ticker or Company Name:", "Tesla")

# Function to fetch news sentiment
def fetch_news_sentiment(ticker):
    news = newsapi.get_everything(q=ticker, language='en', sort_by='relevancy')
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = []
    articles_info = []
    positive_count, negative_count = 0, 0

    for article in news['articles']:
        description = article['description']
        if description:
            score = analyzer.polarity_scores(description)
            sentiment_scores.append(score['compound'])
            sentiment_label = "Positive" if score['compound'] >= 0 else "Negative"

            articles_info.append({
                'Title': article['title'],
                'Source': article['source']['name'],
                'Published': article['publishedAt'][:10],  # Only show YYYY-MM-DD
                'Sentiment': sentiment_label,
                'URL': f"{article['url']}"
            })

            if score['compound'] >= 0:
                positive_count += 1
            else:
                negative_count += 1

    average_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0

    return average_sentiment, articles_info, positive_count, negative_count

# Fetch and Display News Sentiment when the user enters input
if ticker:
    with st.spinner("Fetching latest news..."):
        avg_sentiment, articles, pos_count, neg_count = fetch_news_sentiment(ticker)

    # Sentiment Score Display
    st.subheader(f"📈 Sentiment Analysis for: **{ticker.upper()}**")
    
    sentiment_emoji = "😊" if avg_sentiment > 0 else "😟" if avg_sentiment < 0 else "😐"
    st.metric(label="**Average Sentiment Score**", value=f"{avg_sentiment:.2f}", delta=sentiment_emoji)

    st.progress((avg_sentiment + 1) / 2)  # Normalize -1 to 1 for progress bar

    # Summary Statistics
    st.markdown(f"""
    - 🔹 **Total Articles Analyzed:** {len(articles)}
    - ✅ **Positive Articles:** {pos_count}
    - ❌ **Negative Articles:** {neg_count}
    """)

    # Display Articles in a DataFrame
    if articles:
        df = pd.DataFrame(articles)
        st.dataframe(df, hide_index=True, use_container_width=True)
    else:
        st.warning("No relevant articles found. Try a different keyword.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
    <p>💼 Powered by Advanced Financial Analytics</p>
    </div>
""", unsafe_allow_html=True)
