# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.db.models import F
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver

from django.db import models

# Create your models here.


class Menu(models.Model):
    name = models.CharField(max_length=30)
    left_key = models.IntegerField()
    right_key = models.IntegerField()
    level = models.IntegerField()
    parent_node = models.ForeignKey('self', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_tree(self):
        return self.objects.all().order_by('left_key')

    def get_slave_keys(self, key):
        return self.objects.filter(left_key__gte=key.left_key, right_key__lte=key.right_key).order_by('left_key')

    def get_parent_branch(self, key):
        return self.objects.filter(left_key__lte=key.left_key, rigth_key__gte=key.right_key).order_by('left_key')

    def get_current_branch(self, key):
        return self.objects.filter(left_key__lte=key.left_key, rigth_key__lte=key.right_key, level=key.level + 1).order_by('left_key')

    def get_parent_branch(self, key):
        return self.objects.filter(left_key__lte=key.left_key, rigth_key__gte=key.right_key).order_by('left_key')

    @receiver(post_save, sender=Menu)
    def create_node(self, key, **kwargs):
        parent = key.parent_node
        r_key = parent.right_key
        self.objects.filter(left_key__gt=parent.right_key).update(left_key=F('left_key') + 2, right_key=F('right_key') + 2)
        self.objects.filter(right_key__gte=parent.left_key, left_key__lte=parent.right_key).update(right_key=F('right_key') + 2)
        key.left_key = r_key
        key.left_key = r_key + 1

    @receiver(pre_delete, sender=Menu)
    def create_node(self, key, **kwargs):
        self.objects.filter(left_key__gt=key.right_key, right_key__lt=key.right_key).delete()

        self.objects.filter(left_key__lt=key.left_key, right_key__gt=key.right_key).update(right_key=F('right_key') - (key.right_key - key.left_key + 1))
        self.objects.filter(left_key__gt=key.right_key).update(right_key=F('right_key') - (key.right_key -  key.left_key + 1), left_key=F('left_key') - (key.right_key - key.left_key + 1))






