import pandas as pd
import pytest
from src.financial_analyzer.sentiment import analyze_sentiment


def test_analyze_sentiment():
    """Test the sentiment analysis function."""
    news_data = pd.DataFrame({
        'date': pd.date_range(start='2023-01-01', periods=3),
        'title': [
            'Company reports record profits',
            'Company faces regulatory scrutiny',
            'Company to present at conference'
        ],
        'description': [
            'The company exceeded expectations.',
            'The company is under investigation.',
            'The company will showcase new technology.'
        ],
        'source': ['Source A', 'Source B', 'Source C'],
        'url': ['http://example.com/1', 'http://example.com/2', 'http://example.com/3'],
        'stock': ['AAPL', 'AAPL', 'AAPL']
    })
    
    result = analyze_sentiment(news_data)
    
    assert 'compound' in result.columns
    assert 'positive' in result.columns
    assert 'negative' in result.columns
    assert 'neutral' in result.columns
    assert 'sentiment_category' in result.columns
    
    assert result.iloc[0]['compound'] > 0
    
    assert result.iloc[1]['compound'] < 0
    
    assert not result['sentiment_category
