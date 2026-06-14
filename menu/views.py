from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic import TemplateView
from django.db.models import Sum, Avg

from datetime import date



from .models import Product, Order, OrderItem
from .forms import AddItemForm


class OrderListView(ListView):

    model = Order

    template_name = "menu/order-list.html"

    context_object_name = "orders"

    ordering = ["-created_at"]

    paginate_by = 20


class OrderCreateView(View):
    def get(self, request):
        request.session.pop("last_paid_order", None)
        order = Order.objects.create()
        return redirect("order-detail", pk=order.id)


class OrderDetailView(DetailView):
    model = Order
    template_name = 'menu/order-detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.filter(is_active=True)
        context["form"] = AddItemForm()
        return context


class AddItemView(View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        if order.status == "paid":
            return redirect("order-detail", pk=order.id)

        form = AddItemForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']

            item = OrderItem.objects.filter(
                order=order, product=product
            ).first()

            if item:
                item.quantity += quantity
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
        item = get_object_or_404(OrderItem, pk=pk)
        if item.order.status == "paid":
            return redirect("order-detail", pk=item.order.id)

        item.quantity += 1
        item.save()
        item.order.update_total_price()
        return redirect("order-detail", pk=item.order.id)


class DecreaseQuantityView(View):
    def post(self, request, pk):
        item = get_object_or_404(OrderItem, pk=pk)
        if item.order.status == "paid":
            return redirect("order-detail", pk=item.order.id)

        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()

        item.order.update_total_price()
        return redirect("order-detail", pk=item.order.id)


class DeleteItemView(View):
    def post(self, request, pk):
        item = get_object_or_404(OrderItem, pk=pk)
        if item.order.status == "paid":
            return redirect("order-detail", pk=item.order.id)

        order = item.order
        item.delete()
        order.update_total_price()
        return redirect("order-detail", pk=order.id)


class CompleteOrderView(View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.status = "paid"
        order.save()
        request.session["last_paid_order"] = order.id
        return redirect("payment-success")


class PaymentSuccessView(View):
    def get(self, request):
        return render(request, 'menu/payment-success.html')
    


class DashboardView(TemplateView):

    template_name = "menu/dashboard.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        today = date.today()

        paid_orders = Order.objects.filter(
            status="paid",
            created_at__date=today
        )

        total_sales = (
            paid_orders.aggregate(
                total=Sum("total_price")
            )["total"]
            or 0
        )

        total_orders = paid_orders.count()

        average_order = (
            paid_orders.aggregate(
                avg=Avg("total_price")
            )["avg"]
            or 0
        )

        best_seller = (
            Product.objects
            .filter(
                orderitem__order__status="paid",
                orderitem__order__created_at__date=today,
            )
            .annotate(
                total_sold=Sum("orderitem__quantity")
            )
            .order_by("-total_sold")
            .first()
        )


        context["total_sales"] = total_sales
        context["total_orders"] = total_orders
        context["average_order"] = average_order
        context["best_seller"] = best_seller

        return context