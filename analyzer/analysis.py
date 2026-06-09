import pandas as pd
import numpy as np
from .models import Asset, PriceHistory

def get_asset_dataframe(symbol):
    """
    Fetches price history from the database and converts it to a Pandas DataFrame.
    """
    prices = PriceHistory.objects.filter(asset__symbol=symbol).order_by('timestamp')
    
    if not prices.exists():
        return None

    df = pd.DataFrame(list(prices.values('timestamp', 'close_price', 'volume')))

    df['close_price'] = df['close_price'].astype(float)
    df.set_index('timestamp', inplace=True)
    
    return df

def calculate_technical_indicators(symbol):
    """
    Calculates SMA, RSI, and Daily Returns.
    """
    df = get_asset_dataframe(symbol)
    if df is None or df.empty:
        return f"No data found for {symbol}. Did you run the ingestion script?"

    df['SMA_20'] = df['close_price'].rolling(window=20).mean()
    df['SMA_50'] = df['close_price'].rolling(window=50).mean()

    delta = df['close_price'].diff()

    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()

    rs = gain / loss
    df['RSI_14'] = 100 - (100 / (1 + rs))

    df['Daily_Return_%'] = df['close_price'].pct_change() * 100

    df.dropna(inplace=True)
    
    return df