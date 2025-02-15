from django.urls import path
from . import views

app_name = 'home'  # Thêm namespace cho app

urlpatterns = [
    path('', views.index, name='index'),  # URL cho trang chủ
    path('cart/', views.cart_view, name='cart'),  # URL cho trang giỏ hàng
]