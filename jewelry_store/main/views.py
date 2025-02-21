from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.utils import timezone
from .models import Product, Vang, LichSuGiaVang

def home(request):
    return render(request, 'home.html')

def get_gold_prices(request):
    latest_prices = LichSuGiaVang.objects.filter(
        ngay=timezone.now().date()
    ).select_related('vang')

def get_gold_prices(request):
    data = {"gold_price": 1000}
    return JsonResponse(data)

def gold_prices(request):
    data = [
        {
            "loai_vang": "24k",
            "gia_mua": 68000000,
            "gia_ban": 69000000,
            "ngay": "2025-02-17"
        },
        {
            "loai_vang": "18k",
            "gia_mua": 52000000,
            "gia_ban": 53000000,
            "ngay": "2025-02-17"
        }
    ]
    return JsonResponse(data, safe=False)

def get_products(request):
    products = Product.objects.all()
    data = [
        {
            "code": product.code,
            "name": product.name,
            "category": product.get_category_display(),
            "weight": float(product.weight),
            "price": float(product.price),
            "description": product.description,
            "image": product.image.url if product.image else None,
            "contact_info": product.contact_info,
            "created_at": product.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for product in products
    ]
    return JsonResponse(data, safe=False)

def zyb_tracker_statistics(request):
    return JsonResponse({
        'status': 'success',
        'message': 'Tracking disabled'
    })