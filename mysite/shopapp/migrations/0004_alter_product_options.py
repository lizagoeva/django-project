# Generated by Django 4.2.2 on 2023-06-23 21:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0003_order_products_order_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['price']},
        ),
    ]
