# order_management/views.py  

from django.shortcuts import render, redirect  
from .forms import OrderForm  
from .models import Order  

def create_order(request):  
    if request.method == 'POST':  
        form = OrderForm(request.POST)  
        if form.is_valid():  
            form.save()  
            return redirect('order_list')  # Redirect to order list or another page  
    else:  
        form = OrderForm()  
    return render(request, 'app_QuanLyDonHang/create_order.html', {'form': form})  

def order_list(request):  
    orders = Order.objects.all()  
    return render(request, 'app_QuanLyDonHang/order_list.html', {'orders': orders})