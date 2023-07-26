from django.shortcuts import render, reverse
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Product, Order
from .forms import ProductForm, OrderForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# todo есть вопрос по поводу middleware, который был в задании 5 модуля. Он был написан в приложении fileupload,
#  почему если его подключить в настройках (сейчас он закомментирован), то срабатывать он будет и на запросы
#  shopapp, а не только своего приложения? Он работает на всём проекте? И если это так, то почему его нужно было
#  писать в fileuplod, а не в папке проекта myproject?


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


class ProductListView(ListView):
    queryset = Product.objects.filter(archived=False)
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('shopapp:product_list')


class ProductUpdateView(UpdateView):
    model = Product
    fields = 'name', 'description', 'price', 'discount'
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse(
            'shopapp:product_details',
            kwargs={'pk': self.object.pk},
        )


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('shopapp:product_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrderListView(ListView):
    model = Order
    context_object_name = 'orders'


class OrderDetailView(DetailView):
    queryset = (
        Order.objects
        .select_related('user')
        .prefetch_related('products')
    )


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('shopapp:order_list')


class OrderUpdateView(UpdateView):
    model = Order
    template_name_suffix = '_update_form'
    fields = 'delivery_address', 'user', 'products'

    def get_success_url(self):
        return reverse(
            'shopapp:order_details',
            kwargs={'pk': self.object.pk},
        )


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('shopapp:order_list')
