# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-14 20:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0008_auto_20170514_0342'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='menu_id',
            field=models.IntegerField(null=True),
        ),
    ]
