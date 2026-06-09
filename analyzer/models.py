from django.db import models

class Asset(models.Model):
    ASSET_TYPES = [
        ('STOCK', 'Stock'),
        ('CRYPTO', 'Cryptocurrency'),
    ]
    
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    asset_type = models.CharField(max_length=6, choices=ASSET_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.symbol})"

class PriceHistory(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='prices')
    timestamp = models.DateTimeField()
    open_price = models.DecimalField(max_length=20, decimal_places=4, max_digits=20)
    high_price = models.DecimalField(max_length=20, decimal_places=4, max_digits=20)
    low_price = models.DecimalField(max_length=20, decimal_places=4, max_digits=20)
    close_price = models.DecimalField(max_length=20, decimal_places=4, max_digits=20)
    volume = models.BigIntegerField()

    class Meta:
        ordering = ['-timestamp']
        unique_together = ('asset', 'timestamp')

    def __str__(self):
        return f"{self.asset.symbol} - {self.timestamp.date()} - {self.close_price}"