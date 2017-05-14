# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Menu

from django.shortcuts import render

# Create your views here.


def menu_render(request):
    context = {
        'object_list': Menu.menu_objects.get_tree()
    }
    return render(request, 'menu_list.html', context)


def menu_list(request, menu_item_id):
    print(request)
    object_list = get_object_or_404(Menu, pk=menu_item_id)
    context = {
        'object_list': Menu.menu_objects.get_current_branch(object_list)
    }
    return render(request, 'menu_list.html', context)
