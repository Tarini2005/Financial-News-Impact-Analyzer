# Financial News Impact Analyzer

A Python tool that correlates financial news with market movements using natural language processing.

## Overview

This project analyzes how financial news affects stock prices by:
- Collecting news articles about selected companies
- Analyzing sentiment using NLP techniques
- Correlating news sentiment with stock price movements
- Visualizing the relationships between news and market reactions

## Setup

1. Clone this repository
2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Download NLTK data:
   ```python
   import nltk
   nltk.download('vader_lexicon')
   ```

## Usage

### Basic Example
```python
from src.financial_analyzer.analyzer import FinancialNewsAnalyzer

# Initialize the analyzer
analyzer = FinancialNewsAnalyzer(
    stocks=["AAPL", "MSFT", "GOOGL"],
    start_date="2023-01-01",
    end_date="2023-12-31"
)

# Run analysis
analyzer.run_analysis()

# Generate visualizations
analyzer.visualize_results()
```

### Jupyter Notebooks
Check the `notebooks` directory for detailed examples and visualizations.

## Project Structure

- `src/financial_analyzer/`: Source code
- `notebooks/`: Jupyter notebooks with examples
- `data/`: Data storage
- `tests/`: Test files

## Dependencies

- pandas, numpy, matplotlib, seaborn
- nltk, scikit-learn
- yfinance, requests
- wordcloud, tqdm
