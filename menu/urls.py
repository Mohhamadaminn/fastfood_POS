from django.urls import path
from .views import (
    OrderCreateView, 
    OrderDetailView,
    AddItemView,
    IncreaseQuantityView,
    DecreaseQuantityView,
    DeleteItemView,
    CompleteOrderView,
    PaymentSuccessView,
)


urlpatterns = [
    path('orders/new/', OrderCreateView.as_view(), name='order-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:pk>/add-item/', AddItemView.as_view(), name='add-item'),
    path('item/<int:pk>/increase/', IncreaseQuantityView.as_view(), name='increase-item'),
    path('item/<int:pk>/decrease/', DecreaseQuantityView.as_view(), name='decrease-item'),
    path('item/<int:pk>/delete/', DeleteItemView.as_view(), name='delete-item'),
    path('orders/<int:pk>/complete/', CompleteOrderView.as_view(), name='complete-order'),
    path('payment-success/', PaymentSuccessView.as_view(), name='payment-success'),
]
