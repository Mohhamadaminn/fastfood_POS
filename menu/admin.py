from django.contrib import admin
from . import models


class ProductAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Product, ProductAdmin)

class OrderAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.OrderItem, OrderItemAdmin)