from django.conf.urls import url
from .views import menu_render, menu_list

urlpatterns = [
    url(r'^$', menu_render, name='menu'),
    url(r'^(?P<menu_item_id>\d+)/$', menu_list, name='menu_url'),
]