from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Repurchase, RepurchaseHistory
from django.contrib import messages

@login_required
def repurchase_list(request):
    repurchases = Repurchase.objects.filter(customer=request.user)
    context = {
        'repurchases': repurchases
    }
    return render(request, 'repurchase/repurchase_list.html', context)

@login_required
def create_repurchase(request):
    if request.method == 'POST':
        # Xử lý dữ liệu từ form
        product_name = request.POST.get('product_name')
        product_code = request.POST.get('product_code')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        
        # Tạo yêu cầu mua lại
        repurchase = Repurchase.objects.create(
            customer=request.user,
            product_name=product_name,
            product_code=product_code,
            quantity=quantity,
            price=price
        )
        
        # Tạo lịch sử
        RepurchaseHistory.objects.create(
            repurchase=repurchase,
            action='Created',
            notes='Yêu cầu mua lại mới được tạo'
        )
        
        messages.success(request, 'Yêu cầu mua lại đã được tạo thành công!')
        return redirect('repurchase:list')
        
    return render(request, 'repurchase/create_repurchase.html')

@login_required
def repurchase_detail(request, pk):
    repurchase = Repurchase.objects.get(pk=pk, customer=request.user)
    history = RepurchaseHistory.objects.filter(repurchase=repurchase)
    context = {
        'repurchase': repurchase,
        'history': history
    }
    return render(request, 'repurchase/repurchase_detail.html', context)