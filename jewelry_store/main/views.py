from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

@login_required(login_url='/accounts/login/')
def home(request):
    return render(request, 'products/home.html')

def product_list(request):
    return render(request, 'main/product_list.html')

def product_detail(request, slug):
    return render(request, 'product_detail.html', {'slug': slug})
