import pandas as pd
import pytest
from unittest.mock import patch, MagicMock
from src.financial_analyzer.news_collector import fetch_news, fetch_stock_data, _generate_sample_news


def test_generate_sample_news():
    """Test sample news generation."""
    stocks = ['AAPL', 'MSFT']
    start_date = '2023-01-01'
    end_date = '2023-01-05'
    
    result = _generate_sample_news(stocks, start_date, end_date)
    
    assert isinstance(result, pd.DataFrame)
    
    expected_columns = ['date', 'title', 'description', 'source', 'url', 'stock']
    assert all(col in result.columns for col in expected_columns)

    assert set(result['stock'].unique()).issubset(set(stocks))
    
    min_date = result['date'].min().strftime('%Y-%m-%d')
    max_date = result['date'].max().strftime('%Y-%m-%d')
    assert min_date >= start_date
    assert max_date <= end_date


def test_fetch_news_without_api_key():
    """Test news fetching without API key."""
    stocks = ['AAPL', 'MSFT']
    start_date = '2023-01-01'
    end_date = '2023-01-05'
    
    result = fetch_news(stocks, start_date, end_date)
    
    assert isinstance(result, pd.DataFrame)
    assert not result.empty


@patch('src.financial_analyzer.news_collector.requests.get')
def test_fetch_news_with_api_key(mock_get):
    """Test news fetching with API key."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'articles': [
            {
                'title': 'Test Article',
                'description': 'This is a test',
                'publishedAt': '2023-01-01T12:00:00Z',
                'source': {'name': 'Test Source'},
                'url': 'https://example.com/test'
            }
        ]
    }
    mock_get.return_value = mock_response
    
    stocks = ['AAPL']
    start_date = '2023-01-01'
    end_date = '2023-01-05'
    api_key = 'test_key'
    
    result = fetch_news(stocks, start_date, end_date, api_key)
    
    mock_get.assert_called_once()
    call_args = mock_get.call_args[0][0]
    assert 'AAPL' in call_args
    assert api_key in call_args
    
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert 'Test Article' in result['title'].values


@patch('src.financial_analyzer.news_collector.yf.download')
def test_fetch_stock_data(mock_download):
    """Test stock data fetching."""
    mock_download.return_value = pd.DataFrame({
        'Open': [100.0, 101.0],
        'High': [102.0, 103.0],
        'Low': [98.0, 99.0],
        'Close': [101.0, 102.0],
        'Volume': [1000000, 1100000]
    }, index=pd.date_range(start='2023-01-01', periods=2))
    
    stocks = ['AAPL']
    start_date = '2023-01-01'
    end_date = '2023-01-05'
    
    result = fetch_stock_data(stocks, start_date, end_date)
    
    mock_download.assert_called_once_with(
        'AAPL',
        start=start_date,
        end=end_date,
        progress=False
    )
    assert isinstance(result, dict)
    assert 'AAPL' in result
    assert isinstance(result['AAPL'], pd.DataFrame)
    assert 'Daily_Return' in result['AAPL'].columns
