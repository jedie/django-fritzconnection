from django import template
from django.template.loader import render_to_string

from djfritz.fritz_connection import get_fritz_connection


register = template.Library()


@register.simple_tag(takes_context=True)
def fritzbox_link(context):
    fc = get_fritz_connection()
    if not fc:
        return '<not connected>'

    context = {
        'modelname': fc.modelname,
        'address': fc.soaper.address,
        'system_version': fc.system_version,
    }
    return render_to_string('djfritz/includes/fritzbox_link.html', context)
