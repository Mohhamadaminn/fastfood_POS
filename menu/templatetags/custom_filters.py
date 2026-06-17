from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

@register.filter
def persian_number(value):
    value = intcomma(value, False)

    en = '0123456789,'
    fa = '۰۱۲۳۴۵۶۷۸۹،'

    return str(value).translate(
        str.maketrans(en, fa)
    )