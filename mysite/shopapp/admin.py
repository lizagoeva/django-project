from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
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
