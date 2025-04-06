"""Command-line interface for the Financial News Impact Analyzer."""

import os
import sys
import argparse
from datetime import datetime, timedelta
from .analyzer import FinancialNewsAnalyzer
from .utils import save_results


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Analyze the impact of financial news on stock prices",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument("--stocks", nargs="+", default=["AAPL", "MSFT", "GOOGL"],
                      help="List of stock symbols to analyze")
    parser.add_argument("--start-date", 
                      help="Start date for analysis (YYYY-MM-DD)")
    parser.add_argument("--end-date", 
                      help="End date for analysis (YYYY-MM-DD)")
    parser.add_argument("--api-key", 
                      help="API key for news data (or set NEWS_API_KEY environment variable)")
    
    parser.add_argument("--output-dir", default="results",
                      help="Directory to save results")
    parser.add_argument("--save-data", action="store_true",
                      help="Save data to CSV files")
    parser.add_argument("--no-visualize", action="store_true",
                      help="Skip visualization generation")
    
    # Advanced options
    parser.add_argument("--sentiment-threshold", type=float, default=0.2,
                      help="Threshold for sentiment categorization")
    parser.add_argument("--lag-days", type=int, default=3,
                      help="Number of days to look ahead for price impact")
    
    subparsers = parser.add_subparsers(dest="mode", help="Operation mode")
    
    analysis_parser = subparsers.add_parser("analyze", help="Run standard analysis")
    
    monitor_parser = subparsers.add_parser("monitor", help="Run continuous monitoring")
    monitor_parser.add_argument("--interval", type=int, default=3600,
                              help="Update interval in seconds")
    monitor_parser.add_argument("--duration", type=int,
                              help="Monitoring duration in seconds (omit for indefinite)")
    
    compare_parser = subparsers.add_parser("compare", help="Compare different stocks or sectors")
    compare_parser.add_argument("--sectors", nargs="+", 
                              help="List of sectors to compare (tech, retail, financial, healthcare)")
    
    return parser.parse_args()


def define_sector_stocks(sectors):
    """Define stocks for specified sectors."""
    sector_map = {
        "tech": ["AAPL", "MSFT", "GOOGL", "META", "NVDA"],
        "retail": ["AMZN", "WMT", "TGT", "COST", "HD"],
        "financial": ["JPM", "BAC", "GS", "WFC", "C"],
        "healthcare": ["JNJ", "PFE", "UNH", "MRK", "ABBV"],
        "energy": ["XOM", "CVX", "COP", "EOG", "SLB"],
        "telecom": ["T", "VZ", "TMUS", "CMCSA", "CHTR"]
    }
    
    stocks = []
    for sector in sectors:
        sector = sector.lower()
        if sector in sector_map:
            stocks.extend(sector_map[sector])
        else:
            print(f"Warning: Unknown sector '{sector}'. Available sectors: {', '.join(sector_map.keys())}")
    
    return stocks


def run_monitor_mode(args):
    """Run continuous monitoring mode."""
    from datetime import datetime, timedelta
    import time
    
    api_key = args.api_key or os.environ.get("NEWS_API_KEY", "")
    
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = args.start_date or (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    

    analyzer = FinancialNewsAnalyzer(
        api_key=api_key,
        stocks=args.stocks,
        start_date=start_date,
        end_date=end_date
    )

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    print(f"Starting monitoring for {', '.join(args.stocks)}...")
    print(f"Update interval: {args.interval} seconds")
    if args.duration:
        print(f"Will run for {args.duration} seconds")
    
    start_time = datetime.now()
    iteration = 1
    
    try:
        while True:
            print(f"\n[{datetime.now()}] Monitoring iteration {iteration}")
            
            analyzer.end_date = datetime.now().strftime("%Y-%m-%d")
            analyzer.start_date = args.start_date or (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            

            analyzer.run_analysis()
            
            # Save results if requested
            if args.save_data:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                if not analyzer.news_data.empty:
                    save_results(analyzer.news_data, f"news_data_{timestamp}.csv", args.output_dir)
                    
                if not analyzer.sentiment_data.empty:
                    save_results(analyzer.sentiment_data, f"sentiment_data_{timestamp}.csv", args.output_dir)
            
            if not args.no_visualize:
                analyzer.visualize_results()
            
            if args.duration and (datetime.now() - start_time).total_seconds() >= args.duration:
                print(f"Reached specified duration of {args.duration} seconds. Exiting.")
                break
            
            next_update = datetime.now() + timedelta(seconds=args.interval)
            print(f"Waiting until {next_update.strftime('%Y-%m-%d %H:%M:%S')} for next update...")
            time.sleep(args.interval)
            iteration += 1
    
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")
    
    print("Monitoring complete")


def run_compare_mode(args):
    """Run comparison mode between stocks or sectors."""
    api_key = args.api_key or os.environ.get("NEWS_API_KEY", "")
    

    end_date = args.end_date or datetime.now().strftime("%Y-%m-%d")
    start_date = args.start_date or (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    if args.sectors:
        stocks = define_sector_stocks(args.sectors)
        if not stocks:
            print("Error: No valid sectors specified.")
            return
    else:
        stocks = args.stocks
    
    print(f"Comparing {len(stocks)} stocks: {', '.join(stocks)}")
    
    analyzer = FinancialNewsAnalyzer(
        api_key=api_key,
        stocks=stocks,
        start_date=start_date,
        end_date=end_date
    )
    
    analyzer.run_analysis()
    
    if args.save_data:
        if not os.path.exists(args.output_dir):
            os.makedirs(args.output_dir)
            
        if not analyzer.news_data.empty:
            save_results(analyzer.news_data, "news_data_comparison.csv", args.output_dir)
            
        if not analyzer.sentiment_data.empty:
            save_results(analyzer.sentiment_data, "sentiment_data_comparison.csv", args.output_dir)
            
        if not analyzer.correlation_data.empty:
            save_results(analyzer.correlation_data, "correlation_data_comparison.csv", args.output_dir)
    
    if not args.no_visualize:
        analyzer.visualize_results()
    
    print("Comparison complete")


def run_analyze_mode(args):
    """Run standard analysis mode."""
    api_key = args.api_key or os.environ.get("NEWS_API_KEY", "")
    
    end_date = args.end_date or datetime.now().strftime("%Y-%m-%d")
    start_date = args.start_date or (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    analyzer = FinancialNewsAnalyzer(
        api_key=api_key,
        stocks=args.stocks,
        start_date=start_date,
        end_date=end_date
    )
    
    analyzer.run_analysis()
    
    if args.save_data:
        if not os.path.exists(args.output_dir):
            os.makedirs(args.output_dir)
            
        if not analyzer.news_data.empty:
            save_results(analyzer.news_data, "news_data.csv", args.output_dir)
            
        if not analyzer.sentiment_data.empty:
            save_results(analyzer.sentiment_data, "sentiment_data.csv", args.output_dir)
            
        if not analyzer.correlation_data.empty:
            save_results(analyzer.correlation_data, "correlation_data.csv", args.output_dir)
    
    if not args.no_visualize:
        analyzer.visualize_results()
    
    print("Analysis complete")


def main():
    """Main entry point for the command-line interface."""
    args = parse_args()
    
    if args.mode == "monitor":
        run_monitor_mode(args)
    elif args.mode == "compare":
        run_compare_mode(args)
    else:
        run_analyze_mode(args)


if __name__ == "__main__":
    main()
