import os
import pandas as pd
from datetime import datetime


def save_results(data, filename, directory='results'):
    """
    Save analysis results to a file.
    
    Parameters:
    -----------
    data : pandas.DataFrame
        Data to save
    filename : str
        Filename to save to
    directory : str, optional
        Directory to save in, defaults to 'results'
    """

    if not os.path.exists(directory):
        os.makedirs(directory)
    

    filepath = os.path.join(directory, filename)
    
    # Saving data
    if isinstance(data, pd.DataFrame):
        data.to_csv(filepath, index=False)
    else:
        pd.DataFrame(data).to_csv(filepath, index=False)
    
    print(f"Saved results to {filepath}")


def format_date(date_str):
    """
    Format date string to standard format (YYYY-MM-DD).
    
    Parameters:
    -----------
    date_str : str
        Date string in various formats
        
    Returns:
    --------
    str
        Formatted date string
    """
    try:
        for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d-%m-%Y', '%Y/%m/%d']:
            try:
                return datetime.strptime(date_str, fmt).strftime('%Y-%m-%d')
            except ValueError:
                continue
        
        from dateutil.parser import parse
        return parse(date_str).strftime('%Y-%m-%d')
    
    except Exception as e:
        print(f"Error parsing date '{date_str}': {str(e)}")
        return None


def clean_text(text):
    """
    Clean text data for analysis.
    
    Parameters:
    -----------
    text : str
        Text to clean
        
    Returns:
    --------
    str
        Cleaned text
    """
    if not isinstance(text, str):
        return ""
    
    # Removing HTML tags
    import re
    text = re.sub(r'<.*?>', '', text)
    
    # Removing URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    
    # Removing special characters and digits
    text = re.sub(r'[^\w\s]', '', text)
    
    # Removing extra whitespace
    text = ' '.join(text.split())
    
    return text
