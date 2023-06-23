from django.contrib.auth.models import User
from django.core.management import BaseCommand
from shopapp.models import Order


class Command(BaseCommand):
    """
    Creates orders
    """

    def handle(self, *args, **options):
        self.stdout.write('Приступаем к созданию заказа')
        user = User.objects.get(username='admin')
        order = Order.objects.get_or_create(
            delivery_address='улица Пушкина, дом Колотушкина',
            promocode='SALESALE',
            user=user,
        )
        self.stdout.write(f'Создание заказ: {order}')
        self.stdout.write(f'Заказ создан пользователем: {order[0].user}')
        self.stdout.write(self.style.SUCCESS('Заказ успешно создан'))
