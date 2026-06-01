from django.contrib import admin
from . import models


class ProductAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Product, ProductAdmin)
