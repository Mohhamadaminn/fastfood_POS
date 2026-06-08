from django.urls import path
from .views import (
    OrderCreateView, 
    OrderDetailView,
    AddItemView
)


urlpatterns = [
    path('orders/new/', OrderCreateView.as_view(), name='order-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:pk>/add-item/', AddItemView.as_view(), name='add-item'),
]
