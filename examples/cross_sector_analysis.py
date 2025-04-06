"""Example of creating custom visualizations with the Financial News Impact Analyzer."""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from src.financial_analyzer.analyzer import FinancialNewsAnalyzer


def create_sentiment_volume_impact(analyzer):
    """Create a visualization showing impact of news volume on price volatility."""
    if analyzer.sentiment_data.empty or not analyzer.stock_data:
        print("No data available. Please run analysis first.")
        return
    
    plt.figure(figsize=(12, 8))
    
    # Process each stock
    results = []
    
    for stock in analyzer.stocks:
        if stock not in analyzer.stock_data:
            continue
        
        stock_data = analyzer.stock_data[stock].copy()
        stock_news = analyzer.sentiment_data[analyzer.sentiment_data['stock'] == stock].copy()
        
        if stock_news.empty:
            continue
        
        daily_news = stock_news.groupby(stock_news['date'].dt.date).size().reset_index()
        daily_news.columns = ['date', 'news_count']
        daily_news['date'] = pd.to_datetime(daily_news['date'])
        

        stock_data['volatility'] = (stock_data['High'] - stock_data['Low']) / stock_data['Open'] * 100
        
        merged = pd.merge(stock_data.reset_index(), daily_news, 
                          left_on=stock_data.index.date, right_on='date', 
                          how='left')
        merged['news_count'].fillna(0, inplace=True)
        
        volatility_by_news = merged.groupby('news_count')['volatility'].mean().reset_index()
        
        for _, row in volatility_by_news.iterrows():
            results.append({
                'stock': stock,
                'news_count': row['news_count'],
                'avg_volatility': row['volatility']
            })
    
    # Convert to DataFrame
    results_df = pd.DataFrame(results)
    
    sns.barplot(x='news_count', y='avg_volatility', hue='stock', data=results_df)
    plt.title('Average Daily Volatility by News Volume')
    plt.xlabel('Number of News Articles')
    plt.ylabel('Average Volatility (High-Low as % of Open)')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('volatility_by_news_volume.png', dpi=300)
    plt.show()
    
    return results_df


def create_sentiment_wordcloud_by_category(analyzer):
    """Create word clouds for positive and negative sentiment news."""
    from wordcloud import WordCloud
    
    if analyzer.sentiment_data.empty:
        print("No sentiment data available. Please run analysis first.")
        return
    
    positive_news = analyzer.sentiment_data[analyzer.sentiment_data['sentiment_category'] == 'Positive']
    negative_news = analyzer.sentiment_data[analyzer.sentiment_data['sentiment_category'] == 'Negative']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    if not positive_news.empty:
        positive_text = ' '.join(positive_news['content'].fillna(''))
        wordcloud_positive = WordCloud(background_color='white', max_words=100, 
                                      width=800, height=400, colormap='Greens').generate(positive_text)
        ax1.imshow(wordcloud_positive, interpolation='bilinear')
        ax1.set_title('Positive News Content', fontsize=16)
        ax1.axis('off')
    else:
        ax1.text(0.5, 0.5, 'No positive news data available', 
                horizontalalignment='center', verticalalignment='center', fontsize=12)
        ax1.axis('off')
    
    if not negative_news.empty:
        negative_text = ' '.join(negative_news['content'].fillna(''))
        wordcloud_negative = WordCloud(background_color='white', max_words=100, 
                                      width=800, height=400, colormap='Reds').generate(negative_text)
        ax2.imshow(wordcloud_negative, interpolation='bilinear')
        ax2.set_title('Negative News Content', fontsize=16)
        ax2.axis('off')
    else:
        ax2.text(0.5, 0.5, 'No negative news data available', 
                horizontalalignment='center', verticalalignment='center', fontsize=12)
        ax2.axis('off')
    
    plt.tight_layout()
    plt.savefig('sentiment_wordclouds.png', dpi=300)
    plt.show()


def create_sentiment_timeline(analyzer):
    """Create an interactive timeline of sentiment events."""
    if analyzer.sentiment_data.empty or not analyzer.stock_data:
        print("No data available. Please run analysis first.")
        return
    
    plt.figure(figsize=(14, 8))
    
    for stock in analyzer.stocks:
        if stock in analyzer.stock_data and not analyzer.sentiment_data[
            analyzer.sentiment_data['stock'] == stock].empty:
            example_stock = stock
            break
    else:
        print("No suitable stock data found.")
        return
    
    stock_data = analyzer.stock_data[example_stock].copy()
    stock_news = analyzer.sentiment_data[analyzer.sentiment_data['stock'] == example_stock].copy()
    
    plt.plot(stock_data.index, stock_data['Close'], 'b-', label='Close Price')
    
    for _, news in stock_news.iterrows():
        date = news['date']
        if date in stock_data.index:
            closest_date = stock_data.index[stock_data.index.get_indexer([date], method='nearest')[0]]
            price = stock_data.loc[closest_date, 'Close']
            
            # Determine marker color based on sentiment
            if news['sentiment_category'] == 'Positive':
                color = 'green'
                marker = '^'  # up triangle
            elif news['sentiment_category'] == 'Negative':
                color = 'red'
                marker = 'v'  # down triangle
            else:
                color = 'gray'
                marker = 'o'  # circle
            
            plt.plot(closest_date, price, marker=marker, markersize=10, 
                    color=color, alpha=0.7, markeredgecolor='black')
            
            if abs(news['compound']) > 0.5:
                plt.annotate(f"{news['title'][:30]}...",
                            xy=(closest_date, price),
                            xytext=(10, 10 if news['compound'] > 0 else -10),
                            textcoords='offset points',
                            fontsize=8,
                            arrowprops=dict(arrowstyle='->', color=color))
    
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='^', color='w', markerfacecolor='green', 
              markersize=10, label='Positive News'),
        Line2D([0], [0], marker='v', color='w', markerfacecolor='red', 
              markersize=10, label='Negative News'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', 
              markersize=10, label='Neutral News'),
    ]
    plt.legend(handles=legend_elements, loc='upper left')
    
    plt.title(f'{example_stock} Price with Sentiment Events Timeline')
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('sentiment_timeline.png', dpi=300)
    plt.show()


def create_sentiment_heatmap(analyzer):
    """Create a heatmap of daily sentiment by stock."""
    if analyzer.sentiment_data.empty:
        print("No sentiment data available. Please run analysis first.")
        return
    
    daily_sentiment = analyzer.sentiment_data.groupby(
        [analyzer.sentiment_data['date'].dt.date, 'stock'])['compound'].mean().reset_index()
    
    # Pivot for heatmap format
    pivot_data = daily_sentiment.pivot(index='date', columns='stock', values='compound')
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_data, cmap='coolwarm', center=0, annot=True, fmt='.2f')
    plt.title('Daily Sentiment by Stock')
    plt.xlabel('Stock')
    plt.ylabel('Date')
    plt.tight_layout()
    plt.savefig('sentiment_heatmap.png', dpi=300)
    plt.show()
    
    return pivot_data


def main():
    """Run custom visualizations example."""
    analyzer = FinancialNewsAnalyzer(
        stocks=["AAPL", "MSFT", "GOOGL"],
        start_date="2023-01-01",
        end_date="2023-01-15"
    )
    
    analyzer.run_analysis()
    
    print("\nCreating sentiment volume impact visualization...")
    create_sentiment_volume_impact(analyzer)
    
    print("\nCreating sentiment wordcloud by category...")
    create_sentiment_wordcloud_by_category(analyzer)
    
    print("\nCreating sentiment timeline...")
    create_sentiment_timeline(analyzer)
    
    print("\nCreating sentiment heatmap...")
    create_sentiment_heatmap(analyzer)
    
    print("\nCustom visualizations completed!")


if __name__ == "__main__":
    main()
