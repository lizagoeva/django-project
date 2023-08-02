from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.shortcuts import reverse
from .models import Order
from django.conf import settings


class OrderDetailViewTestCase(TestCase):
    fixtures = [
        'orders-fixture.json',
    ]

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='test order details', password='testpassword')
        permission = Permission.objects.get(codename='view_order')
        cls.user.user_permissions.add(permission)
        cls.user.save()

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)
        Order.objects.filter(delivery_address='test address').delete()
        self.order = Order.objects.create(
            delivery_address='test address',
            promocode='TEST',
            user=self.user,
        )

    def tearDown(self) -> None:
        self.order.delete()

    def test_order_details(self):
        response = self.client.get(reverse('shopapp:order_details', kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        self.assertContains(response, f'Order №{self.order.pk}')


class OrdersExportTestCase(TestCase):
    fixtures = [
        'products-fixture.json',
        'orders-fixture.json',
        'users-fixture.json',
    ]

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='test orders export', password='testexport', is_staff=True)
        cls.aim_url = reverse('shopapp:export_order')
        # todo не уверена, что так можно, но попробовала вынести урл в метод настройки класса

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_orders_export_view(self):
        response = self.client.get(self.aim_url)
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.order_by('pk').all()
        expected_data = [
            {
                'pk': order.pk,
                'delivery_address': order.delivery_address,
                'promocode': order.promocode,
                'user_id': order.user.pk,
                'products_id': [product.pk for product in order.products.all()],
            }
            for order in orders
        ]
        response_data = response.json()
        self.assertEqual(response_data['orders'], expected_data)

    def test_orders_export_not_authenticated(self):
        self.client.logout()
        response = self.client.get(self.aim_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)

    def test_orders_export_not_staff(self):
        self.user.is_staff = False
        self.user.save()
        response = self.client.get(self.aim_url)
        self.assertEqual(response.status_code, 403)
