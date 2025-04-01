"""
Financial News Impact Analyzer - Main example script.

This script demonstrates how to use the Financial News Impact Analyzer
to analyze the relationship between financial news and stock prices.
"""

import os
import argparse
from src.financial_analyzer.analyzer import FinancialNewsAnalyzer
from src.financial_analyzer.utils import save_results


def main():
    """Run the Financial News Impact Analyzer."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Analyze financial news impact on stock prices')
    parser.add_argument('--stocks', nargs='+', default=['AAPL', 'MSFT', 'GOOGL'],
                        help='List of stock symbols to analyze')
    parser.add_argument('--start-date', default=None,
                        help='Start date for analysis (YYYY-MM-DD)')
    parser.add_argument('--end-date', default=None,
                        help='End date for analysis (YYYY-MM-DD)')
    parser.add_argument('--api-key', default=None,
                        help='API key for news data (if not using environment variable)')
    parser.add_argument('--save-dir', default='results',
                        help='Directory to save results')
    args = parser.parse_args()
    
    # Get API key from environment variable if not provided
    api_key = args.api_key or os.environ.get('NEWS_API_KEY', '')
    
    # Initialize the analyzer
    analyzer = FinancialNewsAnalyzer(
        api_key=api_key,
        stocks=args.stocks,
        start_date=args.start_date,
        end_date=args.end_date
    )
    
    # Run analysis
    analyzer.run_analysis()
    
    # Save results
    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)
    
    if not analyzer.news_data.empty:
        save_results(analyzer.news_data, 'news_data.csv', args.save_dir)
    
    if not analyzer.sentiment_data.empty:
        save_results(analyzer.sentiment_data, 'sentiment_data.csv', args.save_dir)
    
    if not analyzer.correlation_data.empty:
        save_results(analyzer.correlation_data, 'correlation_data.csv', args.save_dir)
    
    # Generate visualizations
    analyzer.visualize_results()
    
    print(f"Analysis complete! Results saved to {args.save_dir} directory.")


if __name__ == "__main__":
    main()
