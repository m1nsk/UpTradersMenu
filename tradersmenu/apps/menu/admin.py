# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Menu

from django.contrib import admin

# Register your models here.


class MenuAdmin(admin.ModelAdmin):
    list_display = ['pk','name', 'level', 'parent_node']

admin.site.register(Menu, MenuAdmin)
