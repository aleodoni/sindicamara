# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
	url(r'^estados/$', views.estados, name='estados'),
	url(r'^estado/(?P<id>[0-9]+)/$', views.estado, name='estado'),
	url(r'^cidades/(?P<id>[0-9]+)/$', views.cidades, name='cidades'),
	url(r'^cidade/(?P<id>[0-9]+)/$', views.cidade, name='cidade'),
]