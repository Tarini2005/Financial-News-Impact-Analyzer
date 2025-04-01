import pytest
from src.financial_analyzer.utils import format_date, clean_text


def test_format_date():
    """Test date formatting function."""
    # Test various date formats
    assert format_date('2023-01-15') == '2023-01-15'
    assert format_date('01/15/2023') == '2023-01-15'
    assert format_date('15-01-2023') == '2023-01-15'
    
    # Test invalid date
    assert format_date('invalid-date') is None


def test_clean_text():
    """Test text cleaning function."""
    #HTML removal
    assert clean_text('<p>This is a test</p>') == 'This is a test'
    
    #URL removal
    assert clean_text('Visit https://example.com for more info') == 'Visit  for more info'
    
    #special character removal
    assert clean_text('Hello, world! 123') == 'Hello world 123'
    
    #whitespace handling
    assert clean_text('  Too   many    spaces  ') == 'Too many spaces'
    
    #non-string input
    assert clean_text(None) == ""
    assert clean_text(123) == ""
