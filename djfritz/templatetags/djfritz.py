from django import template
from django.template.loader import render_to_string

from djfritz.views import dynamic_view_menu

register = template.Library()


@register.simple_tag(takes_context=True)
def view_menu(context):
    context = {
        'menu': dynamic_view_menu.menu,
    }
    return render_to_string('djfritz/includes/dynamic_view_menu.html', context)
