from django.shortcuts import redirect
from django.views import View
from django.views.generic import DetailView

from menu.forms import AddItemForm

from .models import Order, OrderItem


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
        context["form"] = AddItemForm() 
        return context
        


