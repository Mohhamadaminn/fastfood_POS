from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic import TemplateView
from django.db.models import Sum, Avg
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.utils.translation import gettext as _
from datetime import date

from .models import Product, Order, OrderItem
from .forms import AddItemForm


class HomeView(LoginRequiredMixin, TemplateView):

    template_name = "home.html"

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

        context["total_sales"] = total_sales
        context["total_orders"] = total_orders

        return context


class OrderListView(LoginRequiredMixin, ListView):

    model = Order

    template_name = "menu/order-list.html"

    context_object_name = "orders"

    ordering = ["-created_at"]

    paginate_by = 20


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        request.session.pop("last_paid_order", None)
        
        order = Order.objects.create(
            user=request.user,
            status='draft'
        )
        return redirect("order-detail", pk=order.id)
    


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'menu/order-detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.filter(is_active=True)
        context["form"] = AddItemForm()
        return context


class AddItemView(LoginRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        
        if order.status in ("paid", "cancelled"):
            return redirect("order-detail", pk=order.id)
        
        form = AddItemForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']
            
            item = OrderItem.objects.filter(order=order, product=product).first()
            
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
            
            if order.status == 'draft':
                order.status = 'open'
                order.save()
            
            order.update_total_price()
            return redirect('order-detail', pk=order.pk)
        
        return redirect('order-detail', pk=order.pk)

class IncreaseQuantityView(LoginRequiredMixin, View):
    def post(self, request, pk):
        item = get_object_or_404(OrderItem, pk=pk)
        if item.order.status in ("paid", "cancelled"):
            return redirect("order-detail", pk=item.order.id)

        item.quantity += 1
        item.save()
        item.order.update_total_price()
        return redirect("order-detail", pk=item.order.id)


class DecreaseQuantityView(LoginRequiredMixin, View):
    def post(self, request, pk):
        item = get_object_or_404(OrderItem, pk=pk)
        if item.order.status in ("paid", "cancelled"):
            return redirect("order-detail", pk=item.order.id)

        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()

        item.order.update_total_price()
        return redirect("order-detail", pk=item.order.id)


class DeleteItemView(LoginRequiredMixin, View):
    def post(self, request, pk):
        item = get_object_or_404(OrderItem, pk=pk)
        if item.order.status in ("paid", "cancelled"):
            return redirect("order-detail", pk=item.order.id)

        order = item.order
        item.delete()
        order.update_total_price()
        return redirect("order-detail", pk=order.id)


class CompleteOrderView(LoginRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)

        if not order.items.exists():
            messages.error(request, _("Your order is empty."))
            return redirect('order-detail', pk=order.pk)



        order.status = "paid"
        order.save()
            
        request.session["last_paid_order"] = order.id
        return redirect("payment-success")


class PaymentSuccessView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'menu/payment-success.html')


class OrderReceiptView(LoginRequiredMixin, DetailView):

    model = Order
    template_name = 'menu/order-receipt.html'
    context_object_name = 'order'


class DashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "menu/dashboard.html"

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()

        # Only real paid orders
        today_paid_orders = Order.objects.filter(
            status="paid",
            created_at__date=today
        )

        total_sales_today = today_paid_orders.aggregate(total=Sum("total_price"))["total"] or 0
        total_orders_today = today_paid_orders.count()
        average_order_today = int(today_paid_orders.aggregate(avg=Avg("total_price"))["avg"]) or 0

        best_seller_today = (
            Product.objects.filter(
                orderitem__order__status="paid",
                orderitem__order__created_at__date=today
            )
            .annotate(total_sold=Sum("orderitem__quantity"))
            .order_by("-total_sold")
            .first()
        )

        all_paid_orders = Order.objects.filter(status="paid")
        total_sales_all = all_paid_orders.aggregate(total=Sum("total_price"))["total"] or 0
        total_paid_orders = all_paid_orders.count()

        open_orders = Order.objects.filter(status="open").count()
        recent_orders = Order.objects.filter(status__in=['open', 'paid']).order_by("-created_at")[:5]

        context.update({
            "total_sales_today": total_sales_today,
            "total_orders_today": total_orders_today,
            "average_order_today": average_order_today,
            "best_seller_today": best_seller_today,
            "total_sales_all": total_sales_all,
            "total_paid_orders": total_paid_orders,
            "open_orders": open_orders,
            "recent_orders": recent_orders,
        })
        return context
    


class CancelOrderView(LoginRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)

        if order.status == "cancelled":
            return redirect("order-detail", pk=order.id)

        order.status = "cancelled"
        order.save()
        return redirect('home')