from django.shortcuts import render
from .models import GoldPrice  # Import model GoldPrice

def gold_price_dashboard(request):
    prices = GoldPrice.objects.order_by('-date')[:30]  # Lấy 30 bản ghi mới nhất
    return render(request, 'gold_price/dashboard.html', {'prices': prices})
