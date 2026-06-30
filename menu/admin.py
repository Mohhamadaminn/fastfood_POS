import jdatetime
jdatetime.set_locale('fa_IR')
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
        'jalali_created_at',
        'status',
        'total_price',
    )
    list_filter = (
        'status',
    )

    def jalali_created_at(self, obj):
        if not obj.created_at:
            return ''
        jalali = jdatetime.datetime.fromgregorian(datetime=obj.created_at)
        return jalali.strftime('%Y/%m/%d - %H:%M')

    jalali_created_at.short_description = 'تاریخ ایجاد'


@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin):
    pass