from django.core.management import BaseCommand
from shopapp.models import Product


class Command(BaseCommand):
    """
    Creates products
    """

    def handle(self, *args, **options):
        self.stdout.write('Приступаем к созданию продуктов')
        product_names = [
            'Шляпа',
            'Шоколадка',
            'Гитара',
            'Машина',
            'Футболка',
        ]
        for product_name in product_names:
            product, created = Product.objects.get_or_create(name=product_name)
            self.stdout.write(f'Добавили продукт: {product.name}')
        self.stdout.write(self.style.SUCCESS('Продукты успешно созданы'))
