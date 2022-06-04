from django.contrib import admin, messages
from django.db.models import Count, QuerySet
from django.urls import reverse
from django.utils.html import format_html, urlencode

from . import models

admin.site.site_header = "Playground Store"
admin.site.index_title = "E-commerce"


class InventoryFilter(admin.SimpleListFilter):
    title = 'Product Inventory'
    parameter_name = 'inventories'

    def lookups(self, request, model_admin):
        return ['<10', 'Low', 'Available']

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ['clear_inventory', 'make_low']
    autocomplete_fields = ['collection']  # This would generate an error on its own unless you enable its class
    # To automatically populate the slug field
    prepopulated_fields = {
        'slug': ['title']
    }
    list_display = ['title', 'price', 'inventory_status', 'collection']
    list_editable = ['price']
    list_per_page = 30
    # list_filter = ['collection', InventoryFilter]
    list_filter = ['collection']

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 20:
            return f'Low: {product.inventory}'
        return f'Available: {product.inventory}'

    @admin.action(description='Clean inventory')
    def clear_inventory(self, request, queryset: QuerySet):
        updated_count = queryset.update(inventory=0)
        self.message_user(request, f'Your actions ({updated_count}) have been carried out!', messages.ERROR)

    @admin.action(description='Make Inventory Low')
    def make_low(self, request, queryset: QuerySet):
        updated_count = queryset.update(inventory=15)
        self.message_user(request, f'Your inventory: {updated_count} has been manipulated as low', messages.SUCCESS)


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_filter = ['membership']
    list_per_page = 20
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__startswith', 'last_name__startswith']


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']  # This was included to stop error in the autocomplete field of product admin

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        params = urlencode({'collection__id': collection.id})
        url = f"{reverse('admin:playground_product_changelist')}?{params}"
        return format_html(f"<a href='{url}'>{collection.products_count}</a>")

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_per_page = 15
    autocomplete_fields = ['customer']  # This worked because it had a search field in the customer admin 
# admin.site.register(models.Collection)
# admin.site.register(models.Product, ProductAdmin)
