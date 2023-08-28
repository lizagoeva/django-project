from django.contrib.sitemaps import Sitemap

from .models import Product, Order


class ShopProductSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.5

    def items(self):
        return Product.objects.filter(archived=False).order_by('name')

    def lastmod(self, obj: Product):
        return obj.creation_time


class ShopOrderSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.5

    def items(self):
        return Order.objects.order_by('creation_time')

    def lastmod(self, obj: Order):
        return obj.creation_time
