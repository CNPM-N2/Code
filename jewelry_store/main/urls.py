from django.urls import path
from . import views
from .views import gold_prices
from django.contrib.auth import views as auth_views

app_name = "main"

urlpatterns = [
    path("", views.home, name="home"),
    path("api/gold-prices/", gold_prices, name='gold-prices'),
    path("api/products/", views.get_products, name="products-list"),
    path('hybridaction/zybTrackerStatisticsAction', views.zyb_tracker_statistics, name='tracker'),
]