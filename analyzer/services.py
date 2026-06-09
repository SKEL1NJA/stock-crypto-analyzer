import yfinance as yf
from datetime import datetime
from .models import Asset, PriceHistory

def fetch_and_save_data(symbol, asset_type, period="30d", interval="1d"):
    """
    Fetches historical data from Yahoo Finance and saves it to the database.
    Example symbols: 'AAPL' for Apple, 'BTC-USD' for Bitcoin.
    """
    ticker = yf.Ticker(symbol)
    info = ticker.info
    name = info.get('longName', symbol)
    
    asset, created = Asset.objects.get_or_create(
        symbol=symbol.upper(),
        defaults={'name': name, 'asset_type': asset_type.upper()}
    )

    df = ticker.history(period=period, interval=interval)
    
    records_saved = 0
    for timestamp, row in df.iterrows():
        # Convert pandas timestamp to python datetime
        dt = timestamp.to_pydatetime()

        price_history, created = PriceHistory.objects.update_or_create(
            asset=asset,
            timestamp=dt,
            defaults={
                'open_price': row['Open'],
                'high_price': row['High'],
                'low_price': row['Low'],
                'close_price': row['Close'],
                'volume': int(row['Volume'])
            }
        )
        if created:
            records_saved += 1
            
    return f"Successfully processed {symbol}. Saved {records_saved} new daily records."