from django.core.management import BaseCommand
from shopapp.models import Order, Product


class Command(BaseCommand):
    """
    Updates orders
    """

    def handle(self, *args, **options):
        order = Order.objects.first()
        if not order:
            self.stdout.write('Заказов не найдено')
            return
        products = Product.objects.all()
        for product in products:
            order.products.add(product)
        order.save()
        self.stdout.write(
            self.style.SUCCESS(f'К заказу {order} добавлены продукты: {order.products.all()}')
        )
