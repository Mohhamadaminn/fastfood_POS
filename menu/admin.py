from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import (
    Product,
    Order,
    OrderItem,
)
 
 
@admin.register(Product)
class ProductAdmin(ModelAdmin):
    pass
 
 
@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'status',
        'total_price',
    )
    list_filter = (
        'status',
    )
 
 
@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin):
    pass
