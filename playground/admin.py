from django.contrib import admin

from . import models

admin.site.site_header = "Playground Store"
admin.site.index_title = "E-commerce"


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price']
    list_editable = ['price']
    list_per_page = 10


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_filter = ['membership']
    ordering = ['first_name', 'last_name']


admin.site.register(models.Collection)
# admin.site.register(models.Product, ProductAdmin)
