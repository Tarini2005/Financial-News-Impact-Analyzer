"""Tests for the visualization module."""

import pandas as pd
import numpy as np
import pytest
from unittest.mock import patch, MagicMock
import matplotlib.pyplot as plt
from src.financial_analyzer.visualization import plot_sentiment_trends, plot_impact_analysis


@pytest.fixture
def sample_sentiment_data():
    """Create sample sentiment data for testing."""
    return pd.DataFrame({
        'date': pd.date_range(start='2023-01-01', periods=10),
        'title': [f'News {i}' for i in range(10)],
        'description': [f'Description {i}' for i in range(10)],
        'stock': ['AAPL', 'AAPL', 'MSFT', 'MSFT', 'GOOGL', 
                 'GOOGL', 'AAPL', 'MSFT', 'GOOGL', 'AAPL'],
        'compound': [0.5, -0.3, 0.8, -0.2, 0.4, 0.1, -0.5, 0.3, -0.1, 0.7],
        'positive': [0.6, 0.2, 0.9, 0.3, 0.5, 0.4, 0.1, 0.5, 0.3, 0.8],
        'negative': [0.1, 0.5, 0.1, 0.5, 0.1, 0.3, 0.6, 0.2, 0.4, 0.1],
        'neutral': [0.3, 0.3, 0.0, 0.2, 0.4, 0.3, 0.3, 0.3, 0.3, 0.1],
        'content': [f'Content {i}' for i in range(10)],
        'sentiment_category': ['Positive', 'Negative', 'Positive', 'Neutral', 'Positive',
                              'Neutral', 'Negative', 'Positive', 'Neutral', 'Positive']
    })


@pytest.fixture
def sample_correlation_data():
    """Create sample correlation data for testing."""
    return pd.DataFrame({
        'stock': ['AAPL', 'MSFT', 'GOOGL'],
        'correlation': [0.35, -0.15, 0.25],
        'avg_sentiment': [0.2, 0.1, 0.3],
        'news_count': [4, 3, 3]
    })


@pytest.fixture
def sample_stock_data():
    """Create sample stock data for testing."""
    stocks = {}
    for symbol in ['AAPL', 'MSFT', 'GOOGL']:
        stocks[symbol] = pd.DataFrame({
            'Open': np.random.uniform(100, 200, 10),
            'High': np.random.uniform(100, 200, 10),
            'Low': np.random.uniform(100, 200, 10),
            'Close': np.random.uniform(100, 200, 10),
            'Volume': np.random.randint(1000000, 2000000, 10)
        }, index=pd.date_range(start='2023-01-01', periods=10))
    return stocks


@patch('matplotlib.pyplot.show')
@patch('matplotlib.pyplot.savefig')
def test_plot_sentiment_trends(mock_savefig, mock_show, sample_sentiment_data):
    """Test sentiment trends visualization function."""
    stocks = ['AAPL', 'MSFT', 'GOOGL']
    
    # Run the function
    plot_sentiment_trends(sample_sentiment_data, stocks)
    
    # Check that savefig was called
    mock_savefig.assert_called_once_with('sentiment_trends.png', dpi=300)
    
    # Check that show was called
    mock_show.assert_called_once()
    
    # Close all plots to avoid affecting other tests
    plt.close('all')


@patch('matplotlib.pyplot.show')
@patch('matplotlib.pyplot.savefig')
def test_plot_impact_analysis(mock_savefig, mock_show, sample_correlation_data, 
                            sample_sentiment_data, sample_stock_data):
    """Test impact analysis visualization function."""
    # Run the function
    plot_impact_analysis(sample_correlation_data, sample_sentiment_data, sample_stock_data)
    
    # Check that savefig was called
    mock_savefig.assert_called_once_with('news_impact_analysis.png', dpi=300)
    
    # Check that show was called
    mock_show.assert_called_once()
    
    # Close all plots to avoid affecting other tests
    plt.close('all')
