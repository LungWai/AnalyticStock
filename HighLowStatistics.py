import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

def get_weekly_ohlc_analysis(ticker_symbol, period="3mo"):
    """
    Fetch historical OHLC data and analyze weekly patterns
    
    Args:
        ticker_symbol (str): Stock ticker symbol
        period (str): Time period for analysis. Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        
    Returns:
        dict: Dictionary containing weekday statistics
    """
    # Fetch data
    ticker = yf.Ticker(ticker_symbol)
    df = ticker.history(period=period)

    # Add weekday information
    df['Weekday'] = df.index.dayofweek
    df['WeekNumber'] = df.index.isocalendar().week
    df['Year'] = df.index.year
    # Create unique week identifier
    df['WeekID'] = df['Year'].astype(str) + '-' + df['WeekNumber'].astype(str)
    
    # Calculate weekly high and low
    weekly_stats = df.groupby('WeekID').agg({
        'High': 'max',
        'Low': 'min'
    }).reset_index()
    
    # Merge back to original dataframe
    df = df.merge(weekly_stats, on='WeekID', suffixes=('', '_week'))
    print(df.head())
    
    # Initialize statistics dictionary
    weekday_stats = {
        'high_freq': {i: 0 for i in range(5)},
        'low_freq': {i: 0 for i in range(5)},
        'total_weeks': len(weekly_stats),
        'weekday_distribution': {i: 0 for i in range(5)}
    }
    
    # Count occurrences of weekly highs and lows
    high_mask = (df['High'] == df['High_week'])
    low_mask = (df['Low'] == df['Low_week'])
    
    weekday_stats['high_freq'].update(df[high_mask]['Weekday'].value_counts().to_dict())
    weekday_stats['low_freq'].update(df[low_mask]['Weekday'].value_counts().to_dict())
    weekday_stats['weekday_distribution'].update(df['Weekday'].value_counts().to_dict())
    
    return weekday_stats

def format_weekday_stats(stats):
    """
    Format the statistics into a readable format
    
    Args:
        stats (dict): Dictionary containing weekday statistics
        
    Returns:
        pd.DataFrame: Formatted statistics
    """
    weekdays = {
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday'
    }
    
    results = []
    total_weeks = stats['total_weeks']
    
    for day in range(5):
        high_freq = stats['high_freq'][day]
        low_freq = stats['low_freq'][day]
        extreme_points = high_freq + low_freq
        extreme_pct = (extreme_points / (total_weeks * 2)) * 100
        high_pct = (high_freq / total_weeks) * 100
        low_pct = (low_freq / total_weeks) * 100
        
        results.append({
            'Weekday': weekdays[day],
            'High_Frequency': high_freq,
            'High_Percentage': f"{high_pct:.2f}%",
            'Low_Frequency': low_freq,
            'Low_Percentage': f"{low_pct:.2f}%",
            'Extreme_Points': extreme_points,
            'Extreme_Percentage': f"{extreme_pct:.2f}%",
            'Total_Occurrences': stats['weekday_distribution'][day],
            'Weeks_Analyzed': total_weeks
        })
    
    df = pd.DataFrame(results)
    
    # Add a summary row with total weeks
    summary_row = pd.DataFrame([{
        'Weekday': f'Total ({total_weeks} weeks)',
        'High_Frequency': df['High_Frequency'].sum(),
        'High_Percentage': '100.00%',
        'Low_Frequency': df['Low_Frequency'].sum(),
        'Low_Percentage': '100.00%',
        'Extreme_Points': df['Extreme_Points'].sum(),
        'Extreme_Percentage': '100.00%',
        'Total_Occurrences': df['Total_Occurrences'].sum(),
        'Weeks_Analyzed': total_weeks
    }])
    
    return pd.concat([df, summary_row], ignore_index=True)

def compare_stocks_extremes(ticker_list, period="3mo"):
    """
    Compare extreme point percentages across multiple stocks
    
    Args:
        ticker_list (list): List of stock ticker symbols
        period (str): Time period for analysis
        
    Returns:
        pd.DataFrame: Matrix of extreme percentages (weekdays x tickers)
    """
    # Initialize empty DataFrame with weekdays as index
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    comparison_df = pd.DataFrame(index=weekdays)
    
    # Analyze each ticker
    for ticker in ticker_list:
        try:
            # Get statistics
            stats = get_weekly_ohlc_analysis(ticker, period)
            results_df = format_weekday_stats(stats)
            
            # Extract extreme percentages (remove % symbol and convert to float)
            extreme_pcts = results_df['Extreme_Percentage'].iloc[:-1].str.rstrip('%').astype(float)
            comparison_df[ticker] = extreme_pcts.values
            
        except Exception as e:
            print(f"Error analyzing {ticker}: {str(e)}")
            comparison_df[ticker] = [np.nan] * 5
    
    return comparison_df

def compare_stocks_highs(ticker_list, period="3mo"):
    """
    Compare high point percentages across multiple stocks
    
    Args:
        ticker_list (list): List of stock ticker symbols
        period (str): Time period for analysis
        
    Returns:
        pd.DataFrame: Matrix of high percentages (weekdays x tickers)
    """
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    comparison_df = pd.DataFrame(index=weekdays)
    
    for ticker in ticker_list:
        try:
            stats = get_weekly_ohlc_analysis(ticker, period)
            results_df = format_weekday_stats(stats)
            
            # Extract high percentages
            high_pcts = results_df['High_Percentage'].iloc[:-1].str.rstrip('%').astype(float)
            comparison_df[ticker] = high_pcts.values
            
        except Exception as e:
            print(f"Error analyzing {ticker}: {str(e)}")
            comparison_df[ticker] = [np.nan] * 5
    
    return comparison_df

def compare_stocks_lows(ticker_list, period="3mo"):
    """
    Compare low point percentages across multiple stocks
    
    Args:
        ticker_list (list): List of stock ticker symbols
        period (str): Time period for analysis
        
    Returns:
        pd.DataFrame: Matrix of low percentages (weekdays x tickers)
    """
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    comparison_df = pd.DataFrame(index=weekdays)
    
    for ticker in ticker_list:
        try:
            stats = get_weekly_ohlc_analysis(ticker, period)
            results_df = format_weekday_stats(stats)
            
            # Extract low percentages
            low_pcts = results_df['Low_Percentage'].iloc[:-1].str.rstrip('%').astype(float)
            comparison_df[ticker] = low_pcts.values
            
        except Exception as e:
            print(f"Error analyzing {ticker}: {str(e)}")
            comparison_df[ticker] = [np.nan] * 5
    
    return comparison_df

# Example usage in HighLowAnalysis.py:
