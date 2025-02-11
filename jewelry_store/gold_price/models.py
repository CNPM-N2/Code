from django.db import models
class GoldPrice(models.Model):
    date = models.DateField()
    buy_price = models.DecimalField(max_digits=10, decimal_places=2)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2)
    world_price = models.DecimalField(max_digits=10, decimal_places=2)