from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MenuConfig(AppConfig):
    name = "menu"
    verbose_name = _("Menu")