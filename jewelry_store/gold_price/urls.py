from django.urls import path
from .views import gold_price_dashboard  # Import view của gold_price

urlpatterns = [
    path('', gold_price_dashboard, name='gold_price_dashboard'),
]
