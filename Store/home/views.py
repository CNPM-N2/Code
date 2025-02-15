from django.shortcuts import render

def index(request):
    return render(request, 'home/index.html')

def cart_view(request):
    template_name = 'home/cart.html'
    return render(request, template_name)