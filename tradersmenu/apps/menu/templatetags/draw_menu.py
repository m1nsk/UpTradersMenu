from django import template
from ..models import Menu
from django.shortcuts import render
from django.shortcuts import get_object_or_404, get_list_or_404

register = template.Library()


@register.inclusion_tag('menu_list.html')
def draw_menu(name):
    object_by_id = get_list_or_404(Menu, name=name)
    context = {
        'object_list': [object_by_id],
        'menu_map': []
    }
    return context
