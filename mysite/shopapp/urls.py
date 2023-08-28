from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    shop_index,
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    OrderListView,
    OrderDetailView,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView,
    OrdersExportView,
    LatestProductsFeed,
)
from .api import (
    ProductViewSet,
    OrderViewSet,
)

app_name = 'shopapp'

routers = DefaultRouter()
routers.register('products', ProductViewSet)
routers.register('orders', OrderViewSet)

urlpatterns = [
    path('', shop_index, name='index'),
    path('api/', include(routers.urls)),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/create/', ProductCreateView.as_view(), name='create_product'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_details'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/archive/', ProductDeleteView.as_view(), name='product_delete'),
    path('products/latest/feed/', LatestProductsFeed(), name='product_feed'),
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('orders/create/', OrderCreateView.as_view(), name='create_order'),
    path('orders/export/', OrdersExportView.as_view(), name='export_order'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_details'),
    path('orders/<int:pk>/update/', OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),
]
