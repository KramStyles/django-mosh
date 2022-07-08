from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from django.contrib.contenttypes.admin import GenericTabularInline

from playground.admin import ProductAdmin
from playground.models import Product
from tags.models import TaggedItem
from .models import User


@admin.register(User)
class UserAdmin(BaseAdmin):
    # We add a new code so we can have new email as required field when creating new user from admin
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name'),
        }),
    )




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
