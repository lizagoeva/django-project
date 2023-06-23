from django.contrib.auth.models import User
from django.db import models


class Product (models.Model):
    class Meta:
        ordering = ['price']
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=False)
    price = models.DecimalField(default=0, max_digits=9, decimal_places=2)
    discount = models.PositiveSmallIntegerField(default=0)
    creation_time = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)


class Order(models.Model):
    delivery_address = models.TextField(blank=True, null=False)
    promocode = models.CharField(blank=True, max_length=8)
    creation_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name='orders')
