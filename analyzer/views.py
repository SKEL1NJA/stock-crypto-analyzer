from django.shortcuts import render
from .analysis import calculate_technical_indicators
from .models import Asset
import json

def dashboard(request, symbol="AAPL"):
    assets = Asset.objects.all()

    df = calculate_technical_indicators(symbol)
    
    context = {
        'assets': assets,
        'selected_symbol': symbol,
        'error': None
    }

    if isinstance(df, str):
        context['error'] = df
    elif df is not None and not df.empty:
        # Get the most recent 30 days of data
        recent_data = df.tail(30).reset_index()
        recent_data['timestamp'] = recent_data['timestamp'].dt.strftime('%Y-%m-%d')

        context['table_data'] = recent_data.to_dict('records')

        context['chart_labels'] = json.dumps(recent_data['timestamp'].tolist())
        context['chart_prices'] = json.dumps(recent_data['close_price'].tolist())
        context['chart_sma20'] = json.dumps(recent_data['SMA_20'].tolist())
    else:
        context['error'] = "No historical data available for this asset."

    return render(request, 'analyzer/dashboard.html', context)