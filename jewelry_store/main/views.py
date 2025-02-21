from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
import requests
from datetime import datetime, timedelta, date
from django.conf import settings
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import *

def home(request):
    san_pham = SanPham.objects.all().prefetch_related(
        'chitietda_set',
        'chitietda_set__da'
    )[:6]
    if request.user.is_authenticated:
        try:
            customer = NguoiDung.objects.get(email=request.user.email)
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        except NguoiDung.DoesNotExist:
            items = []
            order = {'get_cart_items': 0, 'get_cart_total': 0}
            cartItems = order['get_cart_items']
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"

    san_pham = SanPham.objects.all()
    context = {'san_pham_list': san_pham, 'cartItems': cartItems, 'user_not_login': user_not_login, 'user_login': user_login}
    return render(request, 'home.html', context)

def cart(request):
    if request.user.is_authenticated:
        try:
            customer = NguoiDung.objects.get(email=request.user.email)
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        except NguoiDung.DoesNotExist:
            items = []
            order = {'get_cart_items': 0, 'get_cart_total': 0}
            cartItems = order['get_cart_items']
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'cart.html', context)
    
def checkout(request):
    if request.user.is_authenticated:
        try:
            customer = NguoiDung.objects.get(email=request.user.email)
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        except NguoiDung.DoesNotExist:
            items = []
            order = {'get_cart_items': 0, 'get_cart_total': 0}
            cartItems = order['get_cart_items']
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'checkout.html', context)

@csrf_exempt
def processOrder(request):
    transaction_id = datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        try:
            customer = NguoiDung.objects.get(email=request.user.email)
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            total = float(data['form']['total'])
            order.transaction_id = transaction_id

            if total == float(order.get_cart_total):
                order.complete = True
            order.save()

            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'], 
                state=data['shipping']['state'],
                mobile=data['shipping']['mobile']
            )

            return JsonResponse({
                'status': 'success',
                'message': 'Đặt hàng thành công!'
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Vui lòng đăng nhập để đặt hàng'
        }, status=401)

def detail(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer =customer,complete =False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items =[]
        order ={'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
    context= {'items':items,'order':order,'cartItems':cartItems}
    return render(request,'detail.html',context)
    
def search(request):
    if request.method == "POST":
        searchid = request.POST.get('searchid')
        keys = SanPham.objects.filter(name__contains=searchid)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer =customer,complete =False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items =[]
        order ={'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
    san_pham = SanPham.objects.all()
    return render(request,'search.html',{'searchid':searchid,'keys':keys,'san_pham':san_pham,'cartItems':cartItems})

def product_detail(request, ma_sp):
    san_pham = get_object_or_404(SanPham, ma_sp=ma_sp)
    
    chi_tiet_da = ChiTietDa.objects.filter(san_pham=san_pham).select_related('da')
    
    context = {
        'san_pham': san_pham,
        'chi_tiet_da': chi_tiet_da,
    }
    return render(request, 'product_detail.html', context)

def updateItem(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            'status': 'error',
            'message': 'Vui lòng đăng nhập để thêm sản phẩm'
        }, status=401)

    try:
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']
        
        customer = NguoiDung.objects.get(email=request.user.email)
        product = SanPham.objects.get(ma_sp=productId)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
        
        if action == 'add':
            orderItem.quantity += 1
        elif action == 'remove':
            orderItem.quantity -= 1
            
        orderItem.save()
        
        if orderItem.quantity <= 0:
            orderItem.delete()
            
        return JsonResponse({
            'status': 'success',
            'message': 'Đã cập nhật giỏ hàng thành công!',
            'cartCount': order.get_cart_items
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

def get_gold_prices(request):
    period = request.GET.get('period', '7days')
    today = date.today()
    
    if period == '7days':
        start_date = today - timedelta(days=7)
    elif period == '30days':
        start_date = today - timedelta(days=30)
    else:
        start_date = today - timedelta(days=90)
    
    prices = LichSuGiaVang.objects.filter(
        ngay__gte=start_date,
        ngay__lte=today
    ).select_related('vang')
    
    data = []
    current_date = start_date
    while current_date <= today:
        day_prices = prices.filter(ngay=current_date)
        price_data = {
            'date': current_date.isoformat(),
            'prices': {}
        }
        
        for price in day_prices:
            vang_type = price.vang.loai_vang.lower()
            price_data['prices'][vang_type] = {
                'buy': price.gia_mua,
                'sell': price.gia_ban
            }
        
        data.append(price_data)
        current_date += timedelta(days=1)
    
    return JsonResponse(data, safe=False)

def get_specific_date(request, date):
    try:
        query_date = datetime.strptime(date, '%Y-%m-%d').date()
        prices = LichSuGiaVang.objects.filter(
            ngay=query_date
        ).select_related('vang')
        
        price_data = {
            'date': date,
            'prices': {}
        }
        
        for price in prices:
            vang_type = price.vang.loai_vang.lower()
            price_data['prices'][vang_type] = {
                'buy': price.gia_mua,
                'sell': price.gia_ban
            }
        
        return JsonResponse(price_data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def get_week_around_date(request, date):
    try:
        center_date = datetime.strptime(date, '%Y-%m-%d').date()
        start_date = center_date - timedelta(days=3)
        end_date = center_date + timedelta(days=3)
        
        prices = LichSuGiaVang.objects.filter(
            ngay__gte=start_date,
            ngay__lte=end_date
        ).select_related('vang')
        
        data = []
        current_date = start_date
        while current_date <= end_date:
            day_prices = prices.filter(ngay=current_date)
            price_data = {
                'date': current_date.isoformat(),
                'prices': {}
            }
            
            for price in day_prices:
                vang_type = price.vang.loai_vang.lower()
                price_data['prices'][vang_type] = {
                    'buy': price.gia_mua,
                    'sell': price.gia_ban
                }
            
            data.append(price_data)
            current_date += timedelta(days=1)
        
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def fetch_gold_prices():
    headers = {
        'x-access-token': settings.GOLDAPI_KEY,
        'Content-Type': 'application/json'
    }
    
    try:
        # Lấy giá vàng theo USD
        response = requests.get('https://www.goldapi.io/api/XAU/USD', headers=headers)
        print("API Response:", response.text)
        
        if response.status_code == 200:
            data = response.json()
            
            # Lấy giá trực tiếp từ API theo gram
            price_gram_24k = float(data['price_gram_24k'])
            price_gram_18k = float(data['price_gram_18k'])
            price_gram_14k = float(data['price_gram_14k'])
            
            # Chuyển đổi USD sang VND (1 USD = 24,500 VND)
            usd_to_vnd = 24500
            
            # 1 chỉ = 3.75 grams
            chi_to_gram = 3.75
            
            # Tính giá cho các loại vàng (theo chỉ)
            price_24k = price_gram_24k * usd_to_vnd * chi_to_gram
            price_18k = price_gram_18k * usd_to_vnd * chi_to_gram
            price_14k = price_gram_14k * usd_to_vnd * chi_to_gram
            # Tính giá 9K (khoảng 37.5% của 24K)
            price_9k = price_24k * 0.375
            
            # Làm tròn đến hàng nghìn
            def round_price(price):
                return round(price / 1000) * 1000
            
            prices = {
                '24k': {
                    'buy': round_price(price_24k - 50000),
                    'sell': round_price(price_24k)
                },
                '18k': {
                    'buy': round_price(price_18k - 50000),
                    'sell': round_price(price_18k)
                },
                '14k': {
                    'buy': round_price(price_14k - 50000),
                    'sell': round_price(price_14k)
                },
                '9k': {
                    'buy': round_price(price_9k - 50000),
                    'sell': round_price(price_9k)
                }
            }
            
            # Lưu vào database
            for type_key, prices_data in prices.items():
                Vang.objects.update_or_create(
                    loai_vang=type_key.upper(),
                    defaults={
                        'ma_vang': type_key.upper(),
                        'gia_mua': prices_data['buy'],
                        'gia_ban': prices_data['sell'],
                        'ngay_cap_nhat': datetime.now().date()
                    }
                )
            
            return prices
    except Exception as e:
        print(f"Error fetching gold prices: {e}")
    return None

def get_current_prices(request):
    # Thử lấy từ cache trước
    cached_prices = cache.get('gold_prices')
    if cached_prices:
        return JsonResponse(cached_prices)

    try:
        # Nếu không có trong cache, lấy giá mới từ API
        prices = fetch_gold_prices()
        
        if prices:
            price_data = {
                'date': datetime.now().date().isoformat(),
                'prices': prices
            }
            # Lưu vào cache trong 1 giờ
            cache.set('gold_prices', price_data, timeout=3600)
        else:
            # Còn lại giữ nguyên như cũ
            try:
                latest_prices = {
                    '24k': Vang.objects.filter(loai_vang='24K').latest('ngay_cap_nhat'),
                    '18k': Vang.objects.filter(loai_vang='18K').latest('ngay_cap_nhat'),
                    '14k': Vang.objects.filter(loai_vang='14K').latest('ngay_cap_nhat'),
                    '9k': Vang.objects.filter(loai_vang='9K').latest('ngay_cap_nhat'),
                }
                
                price_data = {
                    'date': latest_prices['24k'].ngay_cap_nhat.isoformat(),
                    'prices': {
                        '24k': {'buy': latest_prices['24k'].gia_mua, 'sell': latest_prices['24k'].gia_ban},
                        '18k': {'buy': latest_prices['18k'].gia_mua, 'sell': latest_prices['18k'].gia_ban},
                        '14k': {'buy': latest_prices['14k'].gia_mua, 'sell': latest_prices['14k'].gia_ban},
                        '9k': {'buy': latest_prices['9k'].gia_mua, 'sell': latest_prices['9k'].gia_ban},
                    }
                }
            except Vang.DoesNotExist:
                price_data = {
                    'date': datetime.now().date().isoformat(),
                    'prices': {
                        '24k': {'buy': 0, 'sell': 0},
                        '18k': {'buy': 0, 'sell': 0},
                        '14k': {'buy': 0, 'sell': 0},
                        '9k': {'buy': 0, 'sell': 0},
                    }
                }
        
        return JsonResponse(price_data)
    except Exception as e:
        print(f"Error in get_current_prices: {e}")
        return JsonResponse({
            'date': datetime.now().date().isoformat(),
            'prices': {
                '24k': {'buy': 0, 'sell': 0},
                '18k': {'buy': 0, 'sell': 0},
                '14k': {'buy': 0, 'sell': 0},
                '9k': {'buy': 0, 'sell': 0},
            }
        }) 
def zyb_tracker_statistics(request):
    return JsonResponse({
        'status': 'success',
        'message': 'Tracking disabled'
    })