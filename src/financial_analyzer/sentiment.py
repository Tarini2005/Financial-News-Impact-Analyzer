"""Sentiment analysis for financial news."""

import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from tqdm import tqdm

try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')


def analyze_sentiment(news_data):
    """
    Analyze sentiment of news articles.
    
    Parameters:
    -----------
    news_data : pandas.DataFrame
        DataFrame containing news articles with 'title' and 'description' columns
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with sentiment analysis results
    """
    sentiment_data = news_data.copy()
    
    sia = SentimentIntensityAnalyzer()
    
    financial_lexicon = {
        "upgraded": 3.0,
        "downgraded": -3.0,
        "exceeds expectations": 3.5,
        "misses expectations": -3.5,
        "bullish": 2.5,
        "bearish": -2.5,
        "outperform": 2.0,
        "underperform": -2.0
    }
    
    sia.lexicon.update(financial_lexicon)

    sentiment_data['content'] = sentiment_data['title'] + " " + sentiment_data['description'].fillna("")

    sentiments = []
    for content in tqdm(sentiment_data['content'], desc="Analyzing sentiment"):
        sentiment = sia.polarity_scores(content)
        sentiments.append({
            'compound': sentiment['compound'],
            'positive': sentiment['pos'],
            'negative': sentiment['neg'],
            'neutral': sentiment['neu']
        })
    
    sentiment_df = pd.DataFrame(sentiments)
    result = pd.concat([sentiment_data, sentiment_df], axis=1)
    
    result['sentiment_category'] = pd.cut(
        result['compound'],
        bins=[-1, -0.2, 0.2, 1],
        labels=['Negative', 'Neutral', 'Positive']
    )
    
    return result
