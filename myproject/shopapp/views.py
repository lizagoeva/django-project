from django.shortcuts import render, redirect, reverse
from django.http import HttpRequest, HttpResponse
from .models import Product, Order
from .forms import ProductForm, OrderForm


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


def create_product(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            redirect_url = reverse('shopapp:products_list')
            return redirect(redirect_url)
    else:
        form = ProductForm()
    context = {
        'form': form,
    }
    return render(request, 'shopapp/create-product.html', context=context)


def orders_list(request: HttpRequest):
    context = {
        'orders': Order.objects.prefetch_related('products').select_related('user').all(),
    }
    return render(request, 'shopapp/orders-list.html', context=context)


def create_order(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            redirect_url = reverse('shopapp:orders_list')
            return redirect(redirect_url)
    else:
        form = OrderForm()
    context = {
        'form': form,
    }
    return render(request, 'shopapp/create-order.html', context=context)
