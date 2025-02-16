from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime, timedelta
from .models import Vang, LichSuGiaVang
import requests
from django.conf import settings
from django.core.cache import cache

def get_gold_prices(request):
    period = request.GET.get('period', '7days')
    today = datetime.now().date()
    
    if period == '7days':
        start_date = today - timedelta(days=7)
    elif period == '30days':
        start_date = today - timedelta(days=30)
    else:  # 90days
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