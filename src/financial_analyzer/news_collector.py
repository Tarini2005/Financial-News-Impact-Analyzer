import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import yfinance as yf
from tqdm import tqdm


def fetch_news(stocks, start_date, end_date, api_key=None):
    """
    Fetch financial news data from API or generate sample data.
    
    Parameters:
    -----------
    stocks : list
        List of stock symbols
    start_date : str
        Start date (YYYY-MM-DD)
    end_date : str
        End date (YYYY-MM-DD)
    api_key : str, optional
        API key for news service
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with news data
    """
    if not api_key:
        print("No API key provided. Using sample data.")
        return _generate_sample_news(stocks, start_date, end_date)
    
    all_news = []
    
    for stock in tqdm(stocks, desc="Fetching news"):
        # Example
        url = f"https://newsapi.org/v2/everything?q={stock}&from={start_date}&to={end_date}&language=en&apiKey={api_key}"
        response = requests.get(url)
        
        if response.status_code == 200:
            articles = response.json().get('articles', [])
            for article in articles:
                all_news.append({
                    'date': article.get('publishedAt', '')[:10],
                    'title': article.get('title', ''),
                    'description': article.get('description', ''),
                    'source': article.get('source', {}).get('name', ''),
                    'url': article.get('url', ''),
                    'stock': stock
                })
        else:
            print(f"Error fetching news for {stock}: {response.status_code}")
    
    news_df = pd.DataFrame(all_news)
    
    # Converting date to datetime
    if not news_df.empty:
        news_df['date'] = pd.to_datetime(news_df['date'])
    
    return news_df


def fetch_stock_data(stocks, start_date, end_date):
    """
    Fetch historical stock data using yfinance.
    
    Parameters:
    -----------
    stocks : list
        List of stock symbols
    start_date : str
        Start date (YYYY-MM-DD)
    end_date : str
        End date (YYYY-MM-DD)
        
    Returns:
    --------
    dict
        Dictionary with stock data for each symbol
    """
    stock_data = {}
    
    for stock in tqdm(stocks, desc="Fetching stock data"):
        try:
            # Fetching data using yfinance
            data = yf.download(
                stock, 
                start=start_date,
                end=end_date,
                progress=False
            )
            
            # Calculating daily returns
            data['Daily_Return'] = data['Close'].pct_change() * 100
            
            stock_data[stock] = data
            
        except Exception as e:
            print(f"Error fetching data for {stock}: {str(e)}")
    
    return stock_data


def _generate_sample_news(stocks, start_date, end_date):
    """Generate sample news data for demonstration purposes."""
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Sample news headlines
    positive_news = [
        "reports record profits",
        "exceeds expectations",
        "announces new product",
        "expands into new markets",
        "increases dividend"
    ]
    
    negative_news = [
        "misses earnings expectations",
        "announces layoffs",
        "faces regulatory issues",
        "product recall affects sales",
        "stock downgraded"
    ]
    
    neutral_news = [
        "appoints new board member",
        "to present at conference",
        "releases annual report",
        "announces earnings date",
        "updates corporate policies"
    ]
    
    # Generating sample data
    sample_data = []
    
    for stock in stocks:
        # Generating 1-2 news articles per week for each stock
        for _ in range(int(len(date_range) * 0.2)):
            # Randomly selecting a date
            date = np.random.choice(date_range)
            
            # Randomly selecting news sentiment
            sentiment_type = np.random.choice(['positive', 'negative', 'neutral'], 
                                             p=[0.4, 0.4, 0.2])
            
            if sentiment_type == 'positive':
                headline = f"{stock} {np.random.choice(positive_news)}"
                description = f"The company {np.random.choice(positive_news)}."
            elif sentiment_type == 'negative':
                headline = f"{stock} {np.random.choice(negative_news)}"
                description = f"The company {np.random.choice(negative_news)}."
            else:
                headline = f"{stock} {np.random.choice(neutral_news)}"
                description = f"The company {np.random.choice(neutral_news)}."
            
            sample_data.append({
                'date': date,
                'title': headline,
                'description': description,
                'source': np.random.choice(['MarketWatch', 'Bloomberg', 'CNBC', 'Reuters']),
                'url': f"https://example.com/news/{stock.lower()}-{len(sample_data)}",
                'stock': stock
            })
    
    # Convert to DataFrame and sort by date
    sample_df = pd.DataFrame(sample_data)
    sample_df = sample_df.sort_values('date')
    
    return sample_df
