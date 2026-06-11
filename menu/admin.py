from django.contrib import admin
from .models import(
    Product,
    Order,
    OrderItem,
)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    
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
class OrderItemAdmin(admin.ModelAdmin):
    pass

