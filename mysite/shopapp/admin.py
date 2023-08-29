from io import TextIOWrapper
from csv import DictReader

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path

from .forms import CSVImportForm
from .models import Product, Order, ProductImage


@admin.action(description='Archive products')
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description='Unarchive products')
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


class OrderInline(admin.StackedInline):
    model = Product.orders.through


class ProductImageInline(admin.TabularInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = [
        mark_archived,
        mark_unarchived,
    ]
    inlines = [
        OrderInline,
        ProductImageInline,
    ]
    list_display = 'pk', 'name', 'description_short', 'price', 'discount', 'archived'
    list_display_links = 'pk', 'name'
    ordering = 'price', 'pk'
    search_fields = 'name', 'description', 'discount'
    fieldsets = [
        (None, {
            'fields': ('name', 'description'),
        }),
        ('Price options', {
            'fields': ('price', 'discount'),
            'description': 'Product\'s price info',
        }),
        ('Extra options', {
            'fields': ('archived',),
            'classes': ('collapse',),
            'description': 'Soft delete for product',
        }),
    ]

    def description_short(self, obj: Product) -> str:
        if len(obj.description) > 50:
            return obj.description[:50] + '...'
        return obj.description


class ProductInline(admin.StackedInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    change_list_template = 'shopapp/orders_changelist.html'
    inlines = [
        ProductInline,
    ]
    list_display = 'pk', 'delivery_address', 'promocode', 'datetime_formatted', 'user_verbose'
    list_display_links = 'pk', 'user_verbose'
    ordering = '-creation_time', 'pk'
    search_fields = 'delivery_address', 'pk'
    fieldsets = [
        (None, {
            'fields': ('delivery_address', 'user'),
        }),
        ('Order details', {
            'fields': ('promocode', 'products'),
            'description': 'Some additional info about order',
            'classes': ('collapse',),
        }),
    ]

    def datetime_formatted(self, obj: Order) -> str:
        return obj.creation_time.strftime('%d.%m.%Y, %H:%M')

    def get_queryset(self, request: HttpRequest):
        return Order.objects.select_related('user').prefetch_related('products')

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == 'GET':
            form = CSVImportForm()
            context = {
                'form': form,
            }
            return render(request, 'admin/csv_form.html', context=context)
        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                'form': form,
            }
            return render(request, 'admin/csv_form.html', context=context, status=400)

        csv_file = TextIOWrapper(
            form.files['csv_file'].file,
            encoding=request.encoding,
        )

        csv_reader = DictReader(csv_file)

        orders_data, product_ids = [], []
        fields_to_unpack = ('delivery_address', 'promocode', 'user_id')
        for row in csv_reader:
            orders_data.append(
                {field: row[field] for field in fields_to_unpack}
            )
            products = row['products']
            product_ids.append(list(map(int, products.split(','))))

        orders = [Order(**order_row) for order_row in orders_data]
        Order.objects.bulk_create(orders)

        for order_num in range(len(orders)):
            order_delivery_address = orders[order_num].delivery_address
            order_products = product_ids[order_num]
            Order.objects.filter(delivery_address=order_delivery_address).first().products.set(order_products)

        self.message_user(request, 'Orders data from CSV file imported successfully')
        return redirect('..')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                'import-orders-csv/',
                self.import_csv,
                name='import_orders_csv',
            ),
        ]
        return new_urls + urls
