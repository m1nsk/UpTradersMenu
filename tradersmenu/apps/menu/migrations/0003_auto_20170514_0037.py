# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-13 21:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_auto_20170513_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='parent_node',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='menu.Menu'),
        ),
    ]