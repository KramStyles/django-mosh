from django.contrib import admin

from . import models

admin.site.site_header = "Playground Store"
admin.site.index_title = "E-commerce"


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price']


admin.site.register(models.Collection)
# admin.site.register(models.Product, ProductAdmin)
