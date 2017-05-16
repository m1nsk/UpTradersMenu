# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Menu

from django.shortcuts import render

# Create your views here.


def menu_render(request):
    context = {
        'item_id': ''
    }
    return render(request, 'menu_page.html', context)


def menu_list(request, menu_item_id):
    context = {
        'item_id': menu_item_id
    }
    return render(request, 'menu_page.html', context)