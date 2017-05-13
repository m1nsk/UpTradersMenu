# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from .models import Menu

from django.shortcuts import render

# Create your views here.


def menu_render(request):
    menu = Menu.objects.get(pk=3)
    print(menu.parent_node.parent_node)
    return HttpResponse('hello')
