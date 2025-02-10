from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, ProductInquiry

def home(request):
    featured_products = Product.objects.filter(featured=True)[:6]
    return render(request, 'products/home.html', {
        'featured_products': featured_products
    })

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {
        'product': product
    })

def product_contact(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        ProductInquiry.objects.create(
            product=product,
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            message=request.POST.get('message')
        )
        return redirect('product_detail', product_id=product.id)
    return render(request, 'products/product_contact.html', {'product': product})