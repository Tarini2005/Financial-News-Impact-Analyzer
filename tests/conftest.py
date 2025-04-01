"""Common fixtures for testing the financial news analyzer."""

import pandas as pd
import pytest
from src.financial_analyzer.analyzer import FinancialNewsAnalyzer


@pytest.fixture
def sample_news_data():
    """Return sample news data for testing."""
    return pd.DataFrame({
        'date': pd.date_range(start='2023-01-01', periods=10),
        'title': [f'News title {i}' for i in range(10)],
        'description': [f'News description {i}' for i in range(10)],
        'source': ['Source A'] * 5 + ['Source B'] * 5,
        'url': [f'http://example.com/{i}' for i in range(10)],
        'stock': ['AAPL'] * 5 + ['MSFT'] * 5
    })


@pytest.fixture
def sample_stock_data():
    """Return sample stock data for testing."""
    return {
        'AAPL': pd.DataFrame({
            'Open': [150.0 + i for i in range(10)],
            'High': [155.0 + i for i in range(10)],
            'Low': [145.0 + i for i in range(10)],
            'Close': [152.0 + i for i in range(10)],
            'Volume': [1000000 + i * 10000 for i in range(10)]
        }, index=pd.date_range(start='2023-01-01', periods=10)),
        'MSFT': pd.DataFrame({
            'Open': [250.0 + i for i in range(10)],
            'High': [255.0 + i for i in range(10)],
            'Low': [245.0 + i for i in range(10)],
            'Close': [252.0 + i for i in range(10)],
            'Volume': [2000000 + i * 10000 for i in range(10)]
        }, index=pd.date_range(start='2023-01-01', periods=10))
    }


@pytest.fixture
def sample_sentiment_data(sample_news_data):
    """Return sample sentiment data for testing."""
    sentiment_data = sample_news_data.copy()
    sentiment_data['compound'] = [0.5, -0.3, 0.2, 0.8, -0.5, 0.1, -0.2, 0.3, 0.7, -0.1]
    sentiment_data['positive'] = [0.6, 0.2, 0.4, 0.9, 0.1, 0.3, 0.2, 0.5, 0.8, 0.3]
    sentiment_data['negative'] = [0.1, 0.5, 0.2, 0.1, 0.6, 0.2, 0.4, 0.2, 0.1, 0.4]
    sentiment_data['neutral'] = [0.3, 0.3, 0.4, 0.0, 0.3, 0.5, 0.4, 0.3, 0.1, 0.3]
    sentiment_data['content'] = sentiment_data['title'] + " " + sentiment_data['description']
    sentiment_data['sentiment_category'] = ['Positive', 'Negative', 'Neutral', 'Positive', 'Negative',
                                          'Neutral', 'Neutral', 'Positive', 'Positive', 'Neutral']
    return sentiment_data


@pytest.fixture
def analyzer():
    """Return a FinancialNewsImpactAnalyzer instance for testing."""
    return FinancialNewsAnalyzer(
        stocks=['AAPL', 'MSFT'],
        start_date='2023-01-01',
        end_date='2023-01-10'
    )
