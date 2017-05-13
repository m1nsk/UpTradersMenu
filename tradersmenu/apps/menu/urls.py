from django.conf.urls import url
from .views import menu_render

urlpatterns = [
    url(r'^', menu_render, name='menu')
]