# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Menu

from django.shortcuts import render

# Create your views here.


def menu_render(request):
    context = {
        'object_list': [Menu.menu_objects.filter(level=0)],
        'menu_map': []
    }
    return render(request, 'menu_page.html', context)


def menu_list(request, menu_item_id):
    # it seems to i understood task wrong and you want me to use " models.py -> MenuManager -> get_current_branch " to display the menu_branch
    # so my way was a bit difficult =)
    object_by_id = get_object_or_404(Menu, pk=menu_item_id)
    parent_list = Menu.menu_objects.get_parent_branch(object_by_id)
    object_list = Menu.menu_objects.get_parent_with_child(parent_list)
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
    return render(request, 'menu_page.html', context)