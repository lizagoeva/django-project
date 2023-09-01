import json
import logging

from django.contrib.auth.models import User
from django.contrib.syndication.views import Feed
from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.serializers.json import DjangoJSONEncoder
from django.core.cache import cache

from myauth.models import Profile
from .models import Product, Order
from .forms import ProductForm, OrderForm
from .serializers import OrderSerializer

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


class LatestProductsFeed(Feed):
    title = 'The freshest products'
    description = 'News about adding products or changing the existing ones'
    link = reverse_lazy('shopapp:product_list')

    def items(self):
        return Product.objects.filter(archived=False).order_by('name')[:5]

    def item_title(self, item: Product):
        return item.name

    def item_description(self, item: Product):
        return item.description[:200]

    def item_link(self, item: Product):
        return reverse(
            'shopapp:product_details',
            kwargs={'pk': item.pk},
        )


class UserOrdersListView(LoginRequiredMixin, ListView):
    context_object_name = 'owner'
    template_name = 'shopapp/orders_by_user_list.html'

    def get_queryset(self):
        self.owner = get_object_or_404(User, pk=self.kwargs['user_id'])
        return self.owner

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders_list'] = (
            Order.objects
            .filter(user_id=self.owner.pk)
            .prefetch_related('products')
        )
        context['profile_id'] = Profile.objects.filter(user_id=self.owner.pk).values('pk')[0]['pk']
        return context


class UserOrdersExportView(LoginRequiredMixin, TemplateView):
    template_name = 'shopapp/users_orders_export.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cache_key = f'export_orders_user_{self.kwargs["user_id"]}'
        orders_data_json = cache.get(cache_key)
        if orders_data_json is None:
            user = get_object_or_404(User, pk=self.kwargs['user_id'])
            users_orders = Order.objects.filter(user_id=user.pk).order_by('pk')
            orders_serializer = OrderSerializer(users_orders, many=True)

            encoder = DjangoJSONEncoder()
            orders_data = encoder.encode(orders_serializer.data)
            orders_data_json = json.loads(orders_data)

            cache.set(cache_key, orders_data_json, 300)
        context['orders_json'] = {'orders': orders_data_json}
        return context
