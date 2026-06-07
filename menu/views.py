from django.shortcuts import render
from . import models
from django.views import View, generic
from .models import Product, Order, OrderItem



class OrderShowView(generic.DetailView):
    model = Order
    template_name = "home.html"
    context_object_name = "order"


class NewOrderView(View):

    def get(self, request):

        products = Product.objects.filter(is_active = True)

        return render(
            request,
            'menu/new-order.html',
            {'products': products},
        )
    
    def post(self, request):
        products = Product.objects.filter(is_active=True)

        for product in products:
            quantity = request.POST.get(
                f"product_{product.id}"
            )