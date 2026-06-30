from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    name = models.CharField(_("Name"), max_length=55)
    price = models.PositiveIntegerField(_("Price"))
    is_active = models.BooleanField(_("Active"), default=True)
    image = models.ImageField(
        _("Image"),
        upload_to="products/",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name


class Order(models.Model):

    STATUS_CHOICES = [
        ("draft", _("Draft")),
        ("open", _("Open")),
        ("paid", _("Paid")),
        ("cancelled", _("Cancelled")),
    ]

    user = models.ForeignKey(
        get_user_model(),
        verbose_name=_("User"),
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
    )
    total_price = models.PositiveIntegerField(
        _("Total price"),
        default=0,
    )
    status = models.CharField(
        _("Status"),
        max_length=10,
        choices=STATUS_CHOICES,
        default="draft",
    )

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def update_total_price(self):
        total = 0

        for item in self.items.all():
            total += item.quantity * item.unit_price

        self.total_price = total
        self.save()

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name=_("Order"),
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        Product,
        verbose_name=_("Product"),
        on_delete=models.PROTECT,
    )
    quantity = models.PositiveIntegerField(
        _("Quantity"),
        validators=[MinValueValidator(1)],
    )
    unit_price = models.PositiveIntegerField(
        _("Unit price"),
    )

    class Meta:
        verbose_name = _("Order item")
        verbose_name_plural = _("Order items")

    @property
    def subtotal(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return self.product.name