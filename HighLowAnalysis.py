from HighLowStatistics import get_weekly_ohlc_analysis, format_weekday_stats, compare_stocks_extremes, compare_stocks_highs, compare_stocks_lows

def analyze_stock(ticker_symbol, period="3mo"):
    """
    Analyze stock's weekly high/low patterns
    
    Args:
        ticker_symbol (str): Stock ticker symbol
        period (str): Time period for analysis. Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    """
    try:
        # Get statistics
        stats = get_weekly_ohlc_analysis(ticker_symbol, period)
        
        # Format and display results
        results_df = format_weekday_stats(stats)
        
        # print(f"\nWeekly High/Low Analysis for {ticker_symbol} over period: {period}")
        # print("=" * 80)
        print(results_df[['Weekday', 'Extreme_Points', 'Extreme_Percentage', 'Weeks_Analyzed']].to_string(index=False))
        # print("\nTotal weeks analyzed:", stats['total_weeks'])
        
    except Exception as e:
        print(f"Error analyzing {ticker_symbol}: {str(e)}")

def compare_extremes(tickers, period="3mo"):
    """
    Compare extreme points across multiple stocks
    
    Args:
        tickers (list): List of stock ticker symbols
        period (str): Time period for analysis
        
    Returns:
        pd.DataFrame: Transposed comparison matrix of extreme percentages
    """
    comparison = compare_stocks_extremes(tickers, period)
    return comparison.round(2).transpose()

def compare_highs(tickers, period="3mo"):
    """
    Compare high points across multiple stocks
    
    Args:
        tickers (list): List of stock ticker symbols
        period (str): Time period for analysis
        
    Returns:
        pd.DataFrame: Transposed comparison matrix of high percentages
    """
    comparison = compare_stocks_highs(tickers, period)
    return comparison.round(2).transpose()

def compare_lows(tickers, period="3mo"):
    """
    Compare low points across multiple stocks
    
    Args:
        tickers (list): List of stock ticker symbols
        period (str): Time period for analysis
        
    Returns:
        pd.DataFrame: Transposed comparison matrix of low percentages
    """
    comparison = compare_stocks_lows(tickers, period)
    return comparison.round(2).transpose()

def save_dataframe_to_dat(df, filename):
    try:
        df.to_csv(filename, sep=' ', index=True)
        print(f"DataFrame successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving DataFrame to {filename}: {str(e)}")

# Example usage
if __name__ == "__main__":
    tickers = [
        # Futures
        "YM=F", "ES=F", "NQ=F", "DX-Y.NYB", "GC=F", "CL=F", "BTC-USD",
        
        # Forex
        # "AUDUSD=X", "USDJPY=X", "GBPUSD=X", "GBPJPY=X", "USDCAD=X", "NZDUSD=X", "USDCHF=X", "AUDJPY=X",
        
        # # Stocks
        # "NVDA", "AAPL", "NFLX", "TSLA", "META", "MSFT", "AVGO",
        
        # # ETFs
        # "SMH", "XBI", "XLK", "XLF", "XLY", "XLP", "XLE", "XLI", "XLB", "XLRE", "XLV", "XLU"
    ]

    # extreme_df = compare_extremes(tickers, "2y")
    # highs_df = compare_highs(tickers, "2y")
    lows_df = compare_lows(tickers, "2y")
    # print(highs_df)
    # print("-" * 80)
    # print(lows_df)
    # save_dataframe_to_dat(highs_df, "high_points_analysis.dat")
    save_dataframe_to_dat(lows_df, "low_points_analysis.dat")
    # save_dataframe_to_dat(extreme_df, "extreme_points_analysis.dat")
