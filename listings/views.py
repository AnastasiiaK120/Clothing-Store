from django.shortcuts import render

from .models import Category, Product


def front(request):
    products = Product.objects.all()[:8]
    return render(request, 'product/front.html', {'products': products})


def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'product/shop.html', {'categories': categories, 'products': products})
