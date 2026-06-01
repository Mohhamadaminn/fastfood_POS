from django.shortcuts import render
from django.http import HttpResponse



def showMenu(request):
    return HttpResponse("Helloooo")
