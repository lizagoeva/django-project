from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator


class Product(models.Model):
    class Meta:
        ordering = ['price']

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=False)
    price = models.DecimalField(default=0, max_digits=9, decimal_places=2)
    discount = models.PositiveSmallIntegerField(
        default=0,
        validators=[MaxValueValidator(100)]
    )
    creation_time = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f'Product {self.name!r} with id {self.pk}'


class Order(models.Model):
    delivery_address = models.TextField(blank=True, null=False)
    promocode = models.CharField(blank=True, max_length=8)
    creation_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name='orders')

    def __str__(self) -> str:
        return f'Order №{self.pk} for {self.user}'
