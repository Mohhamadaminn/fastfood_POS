from django.urls import path
from . import views


urlpatterns = [
path('menu/<int:pk>/', views.OrderShowView.as_view(), name='order_show'),
path('new-order/', views.NewOrderView.as_view(), name='new-order'),

]
