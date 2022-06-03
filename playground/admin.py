from django.contrib import admin

from . import models

admin.site.site_header = "Playground Store"
admin.site.index_title = "E-commerce"

admin.site.register(models.Collection)
