import pandas as pd
import pytest
from src.financial_analyzer.analyzer import FinancialNewsAnalyzer


@pytest.fixture
def sample_analyzer():
    """Create a sample analyzer with test data."""
    analyzer = FinancialNewsAnalyzer(
        stocks=['AAPL', 'MSFT'],
        start_date='2023-01-01',
        end_date='2023-01-10'
    )
    
    analyzer.news_data = pd.DataFrame({
        'date': pd.date_range(start='2023-01-01', periods=4),
        'title': [
            'AAPL reports record profits',
            'AAPL faces regulatory scrutiny',
            'MSFT exceeds expectations',
            'MSFT announces layoffs'
        ],
        'description': [
            'The company exceeded expectations.',
            'The company is under investigation.',
            'The company reported strong results.',
            'The company is reducing workforce.'
        ],
        'source': ['Source A', 'Source B', 'Source A', 'Source B'],
        'url': ['http://example.com/1', 'http://example.com/2', 
                'http://example.com/3', 'http://example.com/4'],
        'stock': ['AAPL', 'AAPL', 'MSFT', 'MSFT']
    })
    
    analyzer.stock_data = {
        'AAPL': pd.DataFrame({
            'Open': [150.0, 152.0, 153.0, 155.0],
            'High': [155.0, 154.0, 158.0, 158.0],
            'Low': [149.0, 151.0, 152.0, 155.0],
            'Close': [152.0, 153.0, 156.0, 157.0],
            'Volume': [1000000, 1100000, 1200000, 900000]
        }, index=pd.date_range(start='2023-01-01', periods=4)),
        'MSFT': pd.DataFrame({
            'Open': [250.0, 252.0, 255.0, 258.0],
            'High': [255.0, 257.0, 260.0, 262.0],
            'Low': [248.0, 251.0, 254.0, 257.0],
            'Close': [253.0, 255.0, 259.0, 260.0],
            'Volume': [2000000, 2100000, 2200000, 1900000]
        }, index=pd.date_range(start='2023-01-01', periods=4))
    }
    
    return analyzer


def test_analyzer_initialization():
    """Test analyzer initialization with default values."""
    analyzer = FinancialNewsAnalyzer()
    
    assert isinstance(analyzer.stocks, list)
    assert len(analyzer.stocks) > 0
    assert isinstance(analyzer.start_date, str)
    assert isinstance(analyzer.end_date, str)
    assert analyzer.news_data.empty
    assert len(analyzer.stock_data) == 0


def test_analyze_news_sentiment(sample_analyzer):
    """Test sentiment analysis with sample data."""
    sample_analyzer.analyze_news_sentiment()
    
    assert not sample_analyzer.sentiment_data.empty
    assert len(sample_analyzer.sentiment_data) == 4
    assert 'compound' in sample_analyzer.sentiment_data.columns
    assert 'sentiment_category' in sample_analyzer.sentiment_data.columns


def test_calculate_correlations(sample_analyzer):
    """Test correlation calculation with sample data."""
    sample_analyzer.analyze_news_sentiment()
    
    sample_analyzer.calculate_correlations()
    
    assert not sample_analyzer.correlation_data.empty
    assert len(sample_analyzer.correlation_data) <= 2  
    assert 'stock' in sample_analyzer.correlation_data.columns
    assert 'correlation' in sample_analyzer.correlation_data.columns
    assert 'avg_sentiment' in sample_analyzer.correlation_data.columns
