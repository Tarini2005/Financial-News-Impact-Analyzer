import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

from .news_collector import fetch_news, fetch_stock_data
from .sentiment import analyze_sentiment
from .visualization import plot_sentiment_trends, plot_impact_analysis


class FinancialNewsAnalyzer:
    """Analyze the impact of financial news on stock prices."""
    
    def __init__(self, api_key=None, stocks=None, start_date=None, end_date=None):
        """
        Initialize the Financial News Analyzer.
        
        Parameters:
        -----------
        api_key : str, optional
            API key for the financial news API (e.g., NewsAPI)
        stocks : list, optional
            List of stock symbols to analyze
        start_date : str, optional
            Start date for historical data analysis (YYYY-MM-DD)
        end_date : str, optional
            End date for historical data analysis (YYYY-MM-DD)
        """

        self.api_key = api_key or os.environ.get('NEWS_API_KEY', '')
        self.stocks = stocks or ['AAPL', 'MSFT', 'GOOGL']
        self.start_date = start_date or (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        self.end_date = end_date or datetime.now().strftime('%Y-%m-%d')
        
        self.news_data = pd.DataFrame()
        self.stock_data = {}
        self.sentiment_data = pd.DataFrame()
        self.correlation_data = pd.DataFrame()
        
        print(f"Financial News Analyzer initialized for {len(self.stocks)} stocks from {self.start_date} to {self.end_date}")
    
    def run_analysis(self):
        """Run the complete analysis pipeline."""
        print("Starting analysis...")
        
        self.fetch_data()

        self.analyze_news_sentiment()
        
        self.calculate_correlations()
        
        print("Analysis complete!")
        
    def fetch_data(self):
        """Fetch news and stock data."""
        print("Fetching data...")
        
        self.news_data = fetch_news(
            stocks=self.stocks,
            start_date=self.start_date,
            end_date=self.end_date,
            api_key=self.api_key
        )
        
        self.stock_data = fetch_stock_data(
            stocks=self.stocks,
            start_date=self.start_date,
            end_date=self.end_date
        )
        
        print(f"Fetched {len(self.news_data)} news articles and stock data for {len(self.stock_data)} stocks")
    
    def analyze_news_sentiment(self):
        """Analyze sentiment of news articles."""
        print("Analyzing news sentiment...")
        
        if self.news_data.empty:
            print("No news data available. Please fetch data first.")
            return
        
        self.sentiment_data = analyze_sentiment(self.news_data)
        
        print(f"Analyzed sentiment for {len(self.sentiment_data)} articles")
    
    def calculate_correlations(self):
        """Calculate correlations between news sentiment and stock movements."""
        print("Calculating correlations...")
        
        if self.sentiment_data.empty or not self.stock_data:
            print("Missing data. Please ensure both news and stock data are available.")
            return
        
        correlation_results = []
        
        for stock in self.stocks:
            if stock not in self.stock_data:
                continue
                
            stock_df = self.stock_data[stock].copy()
            stock_news = self.sentiment_data[self.sentiment_data['stock'] == stock].copy()
            
            if stock_news.empty:
                continue
            
            daily_sentiment = stock_news.groupby(stock_news['date'].dt.date).agg({
                'compound': 'mean',
                'title': 'count'
            }).rename(columns={'title': 'news_count'})
            
            daily_sentiment.index = pd.to_datetime(daily_sentiment.index)
            
            combined_data = stock_df.join(daily_sentiment, how='left')

            combined_data['next_day_return'] = combined_data['Close'].pct_change(1).shift(-1) * 100
            
            correlation = combined_data['compound'].corr(combined_data['next_day_return'])
            
            correlation_results.append({
                'stock': stock,
                'correlation': correlation,
                'avg_sentiment': stock_news['compound'].mean(),
                'news_count': len(stock_news)
            })
        
        self.correlation_data = pd.DataFrame(correlation_results)
        
        print(f"Calculated correlations for {len(self.correlation_data)} stocks")
    
    def visualize_results(self):
        """Generate visualizations of the analysis results."""
        print("Generating visualizations...")
        
        if self.sentiment_data.empty:
            print("No sentiment data available. Please run analysis first.")
            return
        
        plot_sentiment_trends(self.sentiment_data, self.stocks)
        plot_impact_analysis(self.correlation_data, self.sentiment_data, self.stock_data)
        
        print("Visualizations created!")
