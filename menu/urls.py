from django.urls import path
from .views import OrderShow


urlpatterns = [
path('menu/<int:pk>/', OrderShow.as_view(), name='order_show'),
]
