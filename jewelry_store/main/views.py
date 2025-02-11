from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .models import Product, Category, CustomerReview
from .forms import UserRegistrationForm, CustomerReviewForm

def home(request):
    featured_products = Product.objects.all()[:5]
    recent_reviews = CustomerReview.objects.order_by('-created_at')[:3]
    return render(request, 'home.html', {
        'featured_products': featured_products,
        'recent_reviews': recent_reviews
    })

def product_list(request):
    categories = Category.objects.all()
    category_slug = request.GET.get('category')
    if category_slug:
        products = Product.objects.filter(category__slug=category_slug)
    else:
        products = Product.objects.all()
    return render(request, 'products/list.html', {
        'categories': categories,
        'products': products
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = CustomerReview.objects.filter(product=product)
    if request.method == 'POST' and request.user.is_authenticated:
        form = CustomerReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            messages.success(request, 'Review added successfully!')
            return redirect('product_detail', slug=slug)
    else:
        form = CustomerReviewForm()
    return render(request, 'products/detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form
    })

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})