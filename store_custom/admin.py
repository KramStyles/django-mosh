from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from playground.admin import ProductAdmin
from playground.models import Product
from tags.models import TaggedItem


# Here we combine features to make each app independent of themselves


class TagInline(GenericTabularInline):
    """
    Trying to display inline features for Tags
    """
    autocomplete_fields = ['tag']
    extra = 1
    model = TaggedItem


admin.site.unregister(Product)


@admin.register(Product)
class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]
