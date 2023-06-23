from django.shortcuts import render
from django.http import HttpRequest
from .models import Product, Order


def shop_index(request: HttpRequest):
    page_urls = {
        'products': request.build_absolute_uri() + 'products/',
        'orders': request.build_absolute_uri() + 'orders/',
    }
    print(page_urls)
    context = {
        'page_urls': page_urls,
    }
    return render(request, 'shopapp/shop-index.html', context=context)


def products_list(request: HttpRequest):
    context = {
        'products': Product.objects.all(),
    }
    return render(request, 'shopapp/products-list.html', context=context)


def orders_list(request: HttpRequest):
    context = {
        'orders': Order.objects.prefetch_related('products').select_related('user').all(),
    }
    return render(request, 'shopapp/orders-list.html', context=context)
