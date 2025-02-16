from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('api/gold-prices/current/', views.get_current_prices, name='current_prices'),
] 