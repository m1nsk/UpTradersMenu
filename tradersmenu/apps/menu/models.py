# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.db.models import F, Q, Max
from django.db.models.signals import post_save, pre_save, post_delete, pre_delete
from django.dispatch import receiver

from django.db import models

# Create your models here.


class MenuManager(models.Manager):

    def get_tree(self):
        return super(MenuManager, self).all().order_by('left_key')

    def get_all_child(self, key):
        return super(MenuManager, self).filter(left_key__gte=key.left_key, right_key__lte=key.right_key).order_by('left_key')

    def get_current_branch(self, key):
        return super(MenuManager, self).filter(left_key__lt=key.right_key, right_key__gt=key.left_key).order_by('left_key')

    def get_first_child(self, key):
        return super(MenuManager, self).filter(parent_key=key).order_by(
            'left_key')

    # return chain of parent menu item
    def get_parent_branch(self, key):
        return super(MenuManager, self).filter(left_key__lte=key.left_key, right_key__gte=key.right_key).order_by(
            'left_key')

    # return parent with closest children
    def get_parent_with_child(self, query, menu_name=''):
        if menu_name:
            my_queryarr = [super(MenuManager, self).filter(level=0, name=menu_name)]
        else:
            my_queryarr = [super(MenuManager, self).filter(level=0)]
        for node in query:
            my_queryarr.append(super(MenuManager, self).filter(parent_node=node).order_by('left_key'))
        return my_queryarr


# menu model
class Menu(models.Model):
    name = models.CharField(max_length=30)
    left_key = models.IntegerField(null=True)
    right_key = models.IntegerField(null=True)
    level = models.IntegerField(null=True)
    parent_node = models.ForeignKey('self', null=True, blank=True)

    objects = models.Manager()
    menu_objects = MenuManager()

    def __str__(self):
        return self.name


# insert new node
@receiver(pre_save, sender=Menu)
def create_node(sender, instance, **kwargs):
    # if not a root menu item
    if instance.parent_node:
        parent = instance.parent_node
        # update following nodes
        Menu.objects.filter(left_key__gt=parent.right_key).update(left_key=F('left_key') + 2, right_key=F('right_key') + 2)
        # update parent nodes
        Menu.objects.filter(right_key__gte=parent.right_key, left_key__lt=parent.right_key).update(right_key=F('right_key') + 2)
        instance.left_key = parent.right_key
        instance.right_key = parent.right_key + 1
        instance.level = parent.level + 1
    # if root menu item
    else:
        # find maximum right key nested set
        max_right_key = Menu.objects.filter(level=0).aggregate(maximum=Max('right_key'))
        max_right_key = max_right_key['maximum']
        # if not a first root item
        if max_right_key:
            instance.left_key = max_right_key + 1
            instance.right_key = max_right_key + 2
            instance.level = 0
        # if first root item
        else:
            instance.left_key = 1
            instance.right_key = 2
            instance.level = 0

# delete node
@receiver(post_delete, sender=Menu)
def delete_node(sender, instance, **kwargs):
    if instance.right_key and instance.left_key:
        Menu.objects.filter(left_key__gt=instance.right_key, right_key__lt=instance.right_key).delete()
        # update following nodes
        Menu.objects.filter(left_key__lt=instance.left_key, right_key__gt=instance.right_key).update(right_key=F('right_key') - (instance.right_key - instance.left_key + 1))
        # update parent nodes
        Menu.objects.filter(left_key__gt=instance.right_key).update(right_key=F('right_key') - (instance.right_key - instance.left_key + 1), left_key=F('left_key') - (instance.right_key - instance.left_key + 1))





