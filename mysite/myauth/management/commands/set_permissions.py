from django.contrib.auth.models import User, Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.get(pk=5)
        # new_group, created = Group.objects.get_or_create(name='new_group')
        group, created = Group.objects.get_or_create(name='products_manager')
        permission_product = Permission.objects.get(codename='add_product',)
        permission_order = Permission.objects.get(codename='view_order',)
        group.permissions.add(permission_product)
        user.groups.add(group)
        user.user_permissions.add(permission_order)

        group.save()
        user.save()
