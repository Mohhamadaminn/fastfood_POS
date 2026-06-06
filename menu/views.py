from django.shortcuts import render
from . import models
from django.views import generic


class OrderShow(generic.DetailView):
    model = models.Order
    template_name = "home.html"
    context_object_name = "order"

    