"""
Модуль с представлениями для API приложения shopapp.

Содержит ViewSet для моделей Product и Order
"""

from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer


@extend_schema(description='Product CRUD viewset')
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над сущностями модели Product.

    Предоставляет полный набор CRUD для товаров
    """

    queryset = (
        Product.objects.all()
        .select_related('created_by')
        .prefetch_related('images')
    )
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        OrderingFilter,
    ]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'discount', 'creation_time']

    @extend_schema(
        summary='Product list',
        description='Returns full list of all the existing products',
    )
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @extend_schema(
        summary='Get product by ID',
        description='Retrieves **product** by its ID, returns **404** if product not found',
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(description='Product with this ID is not found'),
        },
    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

    @extend_schema(
        summary='Create new product',
        description='Creates a new product instance',
    )
    def create(self, *args, **kwargs):
        return super().create(*args, **kwargs)

    @extend_schema(
        summary='Update product',
        description='Updates product info',
    )
    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)

    @extend_schema(
        summary='Product partial update',
        description='Partially updates the current product instance',
    )
    def partial_update(self, *args, **kwargs):
        return super().partial_update(*args, **kwargs)

    @extend_schema(
        summary='Delete product',
        description='Deletes current product instance',
    )
    def destroy(self, *args, **kwargs):
        return super().destroy(*args, **kwargs)


@extend_schema(description='Order CRUD viewset')
class OrderViewSet(ModelViewSet):
    """
    Набор представлений для действий над сущностями модели Order.

    Предоставляет полный набор CRUD для заказов
    """

    queryset = (
        Order.objects.all()
        .select_related('user')
        .prefetch_related('products')
    )
    serializer_class = OrderSerializer
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]
    filterset_fields = ['delivery_address', 'promocode']
    ordering_fields = ['delivery_address', 'creation_time']

    @extend_schema(
        summary='Order list',
        description='Returns full list of all the existing orders',
    )
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @extend_schema(
        summary='Get order by ID',
        description='Retrieves **order** by its ID, returns **404** if order not found',
        responses={
            200: OrderSerializer,
            404: OpenApiResponse(description='Order with this ID is not found'),
        },
    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

    @extend_schema(
        summary='Create new order',
        description='Creates a new order instance',
    )
    def create(self, *args, **kwargs):
        return super().create(*args, **kwargs)

    @extend_schema(
        summary='Update order',
        description='Updates order info',
    )
    def update(self, *args, **kwargs):
        return super().update(*args, **kwargs)

    @extend_schema(
        summary='Order partial update',
        description='Partially updates the current order instance',
    )
    def partial_update(self, *args, **kwargs):
        return super().partial_update(*args, **kwargs)

    @extend_schema(
        summary='Delete order',
        description='Deletes current order instance',
    )
    def destroy(self, *args, **kwargs):
        return super().destroy(*args, **kwargs)
