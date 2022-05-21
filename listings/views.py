from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Category, Product


def front(request):
    products = Product.objects.all()[:8]
    return render(request, 'product/front.html', {'products': products})


def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    active_category = request.GET.get('category', '')

    if active_category:
        products = products.filter(category__slug=active_category)

    return render(request, 'product/shop.html', {'categories': categories, 'active_category': active_category, 'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    return render(request, 'product/product_detail.html', {'product': product})