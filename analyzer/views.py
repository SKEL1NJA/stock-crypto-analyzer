from django.shortcuts import render
from django.http import HttpResponse
from django.core.management import call_command
from .analysis import calculate_technical_indicators
from .models import Asset
from .services import fetch_and_save_data
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
        recent_data = df.tail(30).reset_index()
        recent_data['timestamp'] = recent_data['timestamp'].dt.strftime('%Y-%m-%d')
        
        context['table_data'] = recent_data.to_dict('records')
        context['chart_labels'] = json.dumps(recent_data['timestamp'].tolist())
        context['chart_prices'] = json.dumps(recent_data['close_price'].tolist())
        context['chart_sma20'] = json.dumps(recent_data['SMA_20'].tolist())
    else:
        context['error'] = "No historical data available for this asset. Please trigger a data sync first."

    return render(request, 'analyzer/dashboard.html', context)

def trigger_update(request):
    try:
        if not Asset.objects.exists():
            Asset.objects.create(symbol="AAPL", name="Apple Inc.", asset_type="STOCK")
            Asset.objects.create(symbol="BTC-USD", name="Bitcoin USD", asset_type="CRYPTO")
        
        call_command('update_market_data')
        return HttpResponse("Database successfully seeded and market data updated!")
    except Exception as e:
        return HttpResponse(f"Error during update: {str(e)}", status=500)