from django.core.management.base import BaseCommand
from analyzer.models import Asset
from analyzer.services import fetch_and_save_data

class Command(BaseCommand):
    help = 'Fetches the latest price history for all tracked assets in the database'

    def handle(self, *args, **options):
        assets = Asset.objects.all()
        
        if not assets.exists():
            self.stdout.write(self.style.WARNING("No assets found in the database. Add some first!"))
            return

        self.stdout.write(self.style.SUCCESS(f"Starting update for {assets.count()} asset(s)..."))

        for asset in assets:
            self.stdout.write(f"Updating {asset.symbol}...")
            try:
                result = fetch_and_save_data(asset.symbol, asset.asset_type, period="60d")
                self.stdout.write(self.style.SUCCESS(f"-> {result}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to update {asset.symbol}: {str(e)}"))

        self.stdout.write(self.style.SUCCESS("Market data update workflow completed successfully."))