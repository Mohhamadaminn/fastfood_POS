from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    is_owner = models.BooleanField(_("Owner"), default=False)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")