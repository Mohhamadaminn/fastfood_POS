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

            item = OrderItem.objects.filter(
                order=order,
                product=product,
            ).first()

            if item:
                quantity += quantity

                item.save()

            else:

                OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                unit_price=product.price,
            )

            order.update_total_price()

        return redirect('order-detail', pk=order.pk)




class IncreaseQuantityView(View):

    def post(self, request, pk):

        item = get_object_or_404(
            OrderItem,
            pk=pk
        )

        item.quantity += 1

        item.save()

        item.order.update_total_price()

        return redirect(
            "order-detail",
            pk=item.order.id
        )
    

class DecreaseQuantityView(View):

    def post(self, request, pk):

        item = get_object_or_404(
            OrderItem,
            pk=pk
        )

        if item.quantity > 1:

            item.quantity -= 1

            item.save()

        else:

            item.delete()

        item.order.update_total_price()

        return redirect(
            "order-detail",
            pk=item.order.id
        )
    

class DeleteItemView(View):

    def post(self, request, pk):

        item = get_object_or_404(
            OrderItem,
            pk=pk
        )

        order = item.order

        item.delete()

        order.update_total_price()

        return redirect(
            "order-detail",
            pk=order.id
        )