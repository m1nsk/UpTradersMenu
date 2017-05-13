# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.db.models import F
from django.db.models.signals import post_save, pre_save, post_delete, pre_delete
from django.dispatch import receiver

from django.db import models

# Create your models here.


class Menu(models.Model):
    name = models.CharField(max_length=30)
    left_key = models.IntegerField(null=True)
    right_key = models.IntegerField(null=True)
    level = models.IntegerField(null=True)
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


@receiver(pre_save, sender=Menu)
def create_node(sender, instance, **kwargs):
    print(instance.parent_node, 'node')
    if instance.parent_node:
        parent = instance.parent_node
        print(parent, 'parent')
        # update following nodes
        Menu.objects.filter(left_key__gt=parent.right_key).update(left_key=F('left_key') + 2, right_key=F('right_key') + 2)
        # update parent nodes
        Menu.objects.filter(right_key__gte=parent.right_key, left_key__lt=parent.right_key).update(right_key=F('right_key') + 2)
        instance.left_key = parent.right_key
        instance.right_key = parent.right_key + 1
        instance.level = parent.level + 1
    else:
        instance.left_key = 1
        instance.right_key = 2
        instance.level = 0


@receiver(post_delete, sender=Menu)
def delete_node(sender, instance, **kwargs):
    if instance.right_key and instance.left_key:
        Menu.objects.filter(left_key__gt=instance.right_key, right_key__lt=instance.right_key).delete()

        Menu.objects.filter(left_key__lt=instance.left_key, right_key__gt=instance.right_key).update(right_key=F('right_key') - (instance.right_key - instance.left_key + 1))
        Menu.objects.filter(left_key__gt=instance.right_key).update(right_key=F('right_key') - (instance.right_key - instance.left_key + 1), left_key=F('left_key') - (instance.right_key - instance.left_key + 1))





