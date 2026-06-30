from django.contrib import admin
from .models import CustomUser
from unfold.admin import ModelAdmin


@admin.register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    pass