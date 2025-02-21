from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.home, name="home"),
    path("product/<str:ma_sp>/", views.product_detail, name="product_detail"),
    path('checkout/', views.checkout, name="checkout"),
    path('detail/', views.detail, name="detail"),
    path('cart/', views.cart, name='cart'),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name='process_order'),
    path('api/gold-prices/current/', views.get_current_prices, name='current_prices'),
    path('api/gold-prices/', views.get_gold_prices, name='gold_prices'),
    path('api/gold-prices/date/<str:date>/', views.get_specific_date, name='specific_date'),
    path('api/gold-prices/week/<str:date>/', views.get_week_around_date, name='week_around_date'),
    path('hybridaction/zybTrackerStatisticsAction', views.zyb_tracker_statistics, name='tracker'),
]