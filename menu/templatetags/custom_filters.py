from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
import jdatetime


register = template.Library()

@register.filter
def persian_number(value):
    value = intcomma(value, False)

    en = '0123456789,'
    fa = '۰۱۲۳۴۵۶۷۸۹،'

    return str(value).translate(
        str.maketrans(en, fa)
    )



@register.filter
def to_jalali(value, format_string='%Y/%m/%d - %H:%M'):

    if not value:
        return ''
    jalali = jdatetime.datetime.fromgregorian(datetime=value)
    return jalali.strftime(format_string)