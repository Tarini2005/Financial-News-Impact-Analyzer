import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from wordcloud import WordCloud


def plot_sentiment_trends(sentiment_data, stocks):
    """
    Visualize sentiment trends over time.
    
    Parameters:
    -----------
    sentiment_data : pandas.DataFrame
        DataFrame with sentiment analysis
    stocks : list
        List of stock symbols
    """
    # Seting up the visualization style
    plt.style.use('seaborn-v0_8-darkgrid')
    plt.figure(figsize=(12, 8))
    
    # Plot 1: Sentiment distribution by stock
    plt.subplot(2, 2, 1)
    sns.boxplot(x='stock', y='compound', data=sentiment_data)
    plt.title('Sentiment Distribution by Stock')
    plt.xlabel('Stock')
    plt.ylabel('Compound Sentiment Score')
    plt.grid(True, alpha=0.3)
    
    # Plot 2: Sentiment trend over time
    plt.subplot(2, 2, 2)
    
    # Grouping by date and calculating average sentiment
    daily_sentiment = sentiment_data.groupby(sentiment_data['date'].dt.date).agg({
        'compound': 'mean'
    })
    
    # Converting index to datetime
    daily_sentiment.index = pd.to_datetime(daily_sentiment.index)
    
    # Ploting sentiment
    plt.plot(daily_sentiment.index, daily_sentiment['compound'], 'b-', marker='o', alpha=0.7)
    plt.title('Average Sentiment Trend Over Time')
    plt.xlabel('Date')
    plt.ylabel('Compound Sentiment Score')
    plt.grid(True, alpha=0.3)
    
    # Plot 3: Sentiment category distribution
    plt.subplot(2, 2, 3)
    sentiment_counts = sentiment_data['sentiment_category'].value_counts()
    plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', 
            colors=['lightcoral', 'lightblue', 'lightgreen'])
    plt.title('Sentiment Category Distribution')
    
    # Plot 4: Word cloud of news content
    plt.subplot(2, 2, 4)
    text = ' '.join(sentiment_data['content'].fillna(''))
    wordcloud = WordCloud(background_color='white', max_words=100, width=600, height=400).generate(text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('News Content Word Cloud')
    
    plt.tight_layout()
    plt.savefig('sentiment_trends.png', dpi=300)
    plt.show()


def plot_impact_analysis(correlation_data, sentiment_data, stock_data):
    """
    Visualize the impact of news on stock prices.
    
    Parameters:
    -----------
    correlation_data : pandas.DataFrame
        DataFrame with correlation results
    sentiment_data : pandas.DataFrame
        DataFrame with sentiment analysis
    stock_data : dict
        Dictionary with stock price data
    """
    # Seting up the visualization style
    plt.style.use('seaborn-v0_8-darkgrid')
    plt.figure(figsize=(14, 10))
    
    # Plot 1: Correlation between sentiment and returns
    plt.subplot(2, 2, 1)
    
    # Creating bar chart of correlations
    sns.barplot(x='stock', y='correlation', data=correlation_data)
    plt.title('Correlation: Sentiment vs Next-Day Returns')
    plt.xlabel('Stock')
    plt.ylabel('Correlation Coefficient')
    plt.grid(True, alpha=0.3)
    
    # Adding reference line at zero
    plt.axhline(y=0, color='r', linestyle='--', alpha=0.7)
    
    # Plot 2: Average sentiment by stock
    plt.subplot(2, 2, 2)
    sns.barplot(x='stock', y='avg_sentiment', data=correlation_data)
    plt.title('Average Sentiment by Stock')
    plt.xlabel('Stock')
    plt.ylabel('Average Sentiment Score')
    plt.grid(True, alpha=0.3)
    
    # Plot 3: Example stock with sentiment overlay
    plt.subplot(2, 1, 2)
    
    # Choosing first stock for demonstration
    example_stock = correlation_data['stock'].iloc[0] if not correlation_data.empty else None
    
    if example_stock and example_stock in stock_data:
        # Get stock data
        stock_df = stock_data[example_stock].copy()
        
        # Getting sentiment data for this stock
        stock_sentiment = sentiment_data[sentiment_data['stock'] == example_stock]
        
        # Grouping by date
        daily_sentiment = stock_sentiment.groupby(stock_sentiment['date'].dt.date).agg({
            'compound': 'mean',
        })
        
        # Converting index to datetime
        daily_sentiment.index = pd.to_datetime(daily_sentiment.index)
        
        # Creating twin axes
        fig = plt.gca()
        ax2 = fig.twinx()
        
        # Ploting stock price
        fig.plot(stock_df.index, stock_df['Close'], 'b-', label='Close Price')
        fig.set_ylabel('Price ($)', color='b')
        
        # Ploting sentiment points where available
        sentiment_dates = daily_sentiment.index
        for date in sentiment_dates:
            if date in stock_df.index:
                sentiment_value = daily_sentiment.loc[date, 'compound']
                color = 'green' if sentiment_value > 0 else 'red'
                ax2.scatter([date], [sentiment_value], color=color, s=50, alpha=0.7)
        
        # Adding annotations for significant sentiment points
        if not daily_sentiment.empty:
            # Find max and min sentiment points
            max_sentiment = daily_sentiment['compound'].idxmax()
            min_sentiment = daily_sentiment['compound'].idxmin()
            
            # Annotating if they exist in stock data
            if max_sentiment in stock_df.index:
                max_val = daily_sentiment.loc[max_sentiment, 'compound']
                ax2.annotate(f"+{max_val:.2f}", xy=(max_sentiment, max_val),
                             xytext=(10, 20), textcoords='offset points',
                             arrowprops=dict(arrowstyle='->', color='green'))
            
            if min_sentiment in stock_df.index:
                min_val = daily_sentiment.loc[min_sentiment, 'compound']
                ax2.annotate(f"{min_val:.2f}", xy=(min_sentiment, min_val),
                             xytext=(10, -20), textcoords='offset points',
                             arrowprops=dict(arrowstyle='->', color='red'))
        
        ax2.set_ylabel('Sentiment Score', color='r')
        plt.title(f'{example_stock} Stock Price with News Sentiment Overlay')
        plt.xlabel('Date')
        plt.grid(True, alpha=0.3)
    else:
        plt.text(0.5, 0.5, 'No stock data available for visualization',
                horizontalalignment='center', verticalalignment='center')
    
    plt.tight_layout()
    plt.savefig('news_impact_analysis.png', dpi=300)
    plt.show()
    return result
