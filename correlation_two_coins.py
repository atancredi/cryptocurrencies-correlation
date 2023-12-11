# Find Pearson's correlation between two coins
from datetime import datetime, timedelta

from binance.client import Client
from binance import enums  # To connect to the Binance market data endpoint
import pandas as pd  # To process the data

import argparse

def daily_pct_change(symbol: str, start_date: str) -> pd.Series:
    """
    Return the (symbol)'s daily percentage change from (start_date) up to now.
        Parameters:
                symbol: the pair (base)/(quote) [str]
                start_date: get price data from start_date up to now [str]
        Returns:
                A pandas Series
    """
    ohlcv = client.get_historical_klines(
        symbol, enums.KLINE_INTERVAL_1DAY, start_date
    )
    change = [
        (float(entry[4]) - float(entry[1]))/float(entry[1]) for entry in ohlcv
    ]
    #  entry[1]: open price | entry[4]: close price
    
    return pd.Series(change, dtype='float64')

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("symbol1", type=str)
    parser.add_argument("symbol2", type=str)
    args = parser.parse_args()
    symbol1 = args.symbol1+"USDT"
    symbol2 = args.symbol2+"USDT"

    print(f'Computing Pearson\'s Correlation between {symbol1} and {symbol2}.')
    print("\n")

    client = Client()
    _now = datetime.now()
    start_day = (_now - timedelta(days=365)).strftime(r'%Y-%m-%d')
    print(f'Data from {start_day} up to {str(_now)}.')

    changes_1 = daily_pct_change(symbol1, start_day)
    print(changes_1)
    changes_2 = daily_pct_change(symbol2, start_day)
    print(changes_2)
    corr = changes_1.corr(changes_2, min_periods=300)

    print(f"Pearson's correlation between {symbol1} and {symbol2}:", corr)
