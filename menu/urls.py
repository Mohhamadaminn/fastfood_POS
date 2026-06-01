from django.urls import path
from . import views


urlpatterns = [
path('', views.showMenu, name='menu'),
]
