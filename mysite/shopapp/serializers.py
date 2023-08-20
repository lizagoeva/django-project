from rest_framework.serializers import ModelSerializer

from .models import Product, Order


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'pk',
            'name',
            'description',
            'price',
            'discount',
            'creation_time',
            'archived',
            'created_by',
            'images',
        ]


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'pk',
            'delivery_address',
            'promocode',
            'creation_time',
            'user',
            'products',
        ]
