from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    """
    Модель Product представляет сущность товара для продажи в интернет-магазине

    Перейти к модели заказа: :model:`shopapp.Order`
    """
    class Meta:
        ordering = ['price']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

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


def product_images_directory_path(instance: 'ProductImage', filename: str) -> str:
    return 'products/product_{pk}/images/{filename}'.format(
        pk=instance.product.pk,
        filename=filename,
    )


class ProductImage(models.Model):
    """
    Модель ProductImage представляет изображение товара

    Модель продукта: :model:`shopapp.Product`
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=product_images_directory_path)
    description = models.CharField(max_length=200, null=True, blank=True)


class Order(models.Model):
    """
    Модель Order представляет сущность заказа в интернет-магазине

    Перейти к модели продукта: :model:`shopapp.Product`
    """
    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    delivery_address = models.TextField(blank=True, null=False)
    promocode = models.CharField(blank=True, max_length=8)
    creation_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, related_name='orders')

    def __str__(self) -> str:
        return f'Order №{self.pk} for {self.user}'
