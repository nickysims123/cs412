# File: restaurant/urls.py
# Author: Nicholas Sima (nicksima@bu.edu)
# Description: the urls file to redirect all traffic in restaurant app

from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path(r'', views.main, name='main'),
    path(r'order', views.order, name='order'),
    path(r'confirmation', views.confirmation, name='confirmation'),
]
