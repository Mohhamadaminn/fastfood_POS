from django.db import models
from django.core.validators import MinValueValidator


class Product(models.Model):
    name = models.CharField(max_length=55)
    price = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)


    def __str__(self):
        return f"{self.name}"
    

class Order(models.Model):

 #   STATUS_CHOICES=[
 #       ('open', 'open'),
 #       ('paid', 'paid'),
 #   ]


    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.PositiveIntegerField(default=0)
 #   status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=1)

    
    def update_total_price(self):
        total = 0

        for item in self.items.all():
            total += item.quantity * item.unit_price

        self.total_price = total
        self.save()



    def __str__(self):
        return f"Order #{self.id}"
       


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    unit_price = models.PositiveIntegerField()


    @property
    def subtotal(self):
        return self.quantity * self.unit_price
    


    def __str__(self):
        return f"{self.product.name}"
    
