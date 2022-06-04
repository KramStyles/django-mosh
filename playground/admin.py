from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode

from . import models

admin.site.site_header = "Playground Store"
admin.site.index_title = "E-commerce"


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'inventory_status', 'collection']
    list_editable = ['price']
    list_per_page = 30

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 20:
            return f'Low: {product.inventory}'
        return f'Available: {product.inventory}'


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_filter = ['membership']
    ordering = ['first_name', 'last_name']


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        params = urlencode({'collection__id': collection.id})
        url = f"{reverse('admin:playground_product_changelist')}?{params}"
        return format_html(f"<a href='{url}'>{collection.products_count}</a>")

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )

# admin.site.register(models.Collection)
# admin.site.register(models.Product, ProductAdmin)
