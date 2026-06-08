from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView

from menu.forms import AddItemForm
from .forms import AddItemForm
from .models import Product, Order, OrderItem



class OrderCreateView(View):
    
    def get(self, request):

        order = Order.objects.create()

        return redirect('order-detail', pk=order.pk)
    

class OrderDetailView(DetailView):

    model = Order 
    template_name = 'menu/order-detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.filter(
            is_active=True
        )
        context["form"] = AddItemForm() 
        return context



class AddItemView(View):

    def post(self, request, pk):

        order = get_object_or_404(Order, pk=pk)

        form = AddItemForm(request.POST)

        if form.is_valid():

            # using cleaned_data help us to give correct values to our objects.
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                unit_price=product.price,
            )

            order.update_total()

        return redirect('order-detail', pk=order.pk)


