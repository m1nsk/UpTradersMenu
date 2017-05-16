from django import template
from ..models import Menu
from django.shortcuts import render
from django.shortcuts import get_object_or_404, get_list_or_404

register = template.Library()


@register.inclusion_tag('menu_list.html')
def draw_menu(name, id):
    if id:
        menu_item_id = id
        # it seems to i understood task wrong and you want me to use " models.py -> MenuManager -> get_current_branch " to display the menu_branch
        object_by_id = get_object_or_404(Menu, pk=menu_item_id)
        parent_list = Menu.menu_objects.get_parent_branch(object_by_id)
        object_list = Menu.menu_objects.get_parent_with_child(parent_list, name)
        menu_map = [object_by_id.id]
        parent = object_by_id.parent_node
        if parent:
            while parent.parent_node:
                menu_map.append(parent.id)
                parent = parent.parent_node
            menu_map.append(parent.id)

        context = {
            'object_list': object_list,
            'menu_map': menu_map,
            'active_item': object_by_id
        }
        return context
    else:
        context = {
            'object_list': [Menu.menu_objects.filter(level=0, name=name)],
            'menu_map': []
        }
        return context
