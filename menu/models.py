from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=55)
    price = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.name}"
    

class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.PositiveIntegerField(default=0)


    def __str__(self):
        return f"Order #{self.id}"
    
    
    def update_total(self):
        total = 0

        for item in self.items.all():
            total += item.quantity * item.unit_price

        self.total_price = total
        self.save()
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    unit_price = models.PositiveIntegerField()


    def __str__(self):
        return f"{self.product.name}"