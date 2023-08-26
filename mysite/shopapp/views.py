import logging

from django.shortcuts import render, reverse
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

from .models import Product, Order
from .forms import ProductForm, OrderForm

logger = logging.getLogger(__name__)


def shop_index(request: HttpRequest):
    logger.info('Called shop index view')
    page_urls = {
        'products': request.build_absolute_uri() + 'products/',
        'orders': request.build_absolute_uri() + 'orders/',
    }
    print(page_urls)
    context = {
        'page_urls': page_urls,
    }
    logger.debug('Rendering shop index template with the context: %s', context)
    return render(request, 'shopapp/shop-index.html', context=context)


class ProductListView(ListView):
    queryset = Product.objects.filter(archived=False)
    context_object_name = 'products'

    def get(self, *args, **kwargs):
        logger.info('Called products list view')
        return super().get(*args, **kwargs)


class ProductDetailView(LoginRequiredMixin, DetailView):
    queryset = Product.objects.prefetch_related('images')


class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'shopapp.add_product'
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('shopapp:product_list')

    def form_valid(self, form):
        logger.info('Product created')
        logger.debug('Form is valid, new product data: %s', form.cleaned_data)
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        logger.info('Called product update view')
        if self.request.user.is_superuser:
            return True
        product_creator = self.get_object().created_by
        return self.request.user.has_perm('shopapp.change_product') and product_creator == self.request.user

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
        logger.info('Product №%s archived', self.object.pk)
        logger.debug(
            'Product №%s successfully archived, redirect to %s',
            self.object.pk,
            success_url,
        )
        return HttpResponseRedirect(success_url)


class OrderListView(ListView):
    model = Order
    context_object_name = 'orders'

    def get(self, *args, **kwargs):
        logger.info('Called orders list view')
        return super().get(*args, **kwargs)


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

    def get_form(self, *args, **kwargs):
        form = super(OrderCreateView, self).get_form(*args, **kwargs)
        form.fields['products'].queryset = Product.objects.filter(archived=False)
        return form

    def form_valid(self, form):
        logger.info('Order created')
        logger.debug('Form is valid, new order data: %s', form.cleaned_data)
        return super().form_valid(form)


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

    def form_valid(self, form):
        success_url = self.get_success_url()
        logger.info('Order №%s archived', self.object.pk)
        logger.debug(
            'Order №%s successfully archived, redirect to %s',
            self.object.pk,
            success_url,
        )
        return HttpResponseRedirect(success_url)


class OrdersExportView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request: HttpRequest) -> JsonResponse:
        logger.info('Called orders export view')
        orders = Order.objects.order_by('pk').all()
        orders_data = [
            {
                'pk': order.pk,
                'delivery_address': order.delivery_address,
                'promocode': order.promocode,
                'user_id': order.user.pk,
                'products_id': [product.pk for product in order.products.all()],
            }
            for order in orders
        ]
        logger.debug('Returning orders info: %s', orders_data)
        return JsonResponse({'orders': orders_data})
