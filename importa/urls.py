# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^cadastro/$', views.cadastro, name='cadastro'),
	url(r'^contribuicoes/$', views.contribuicoes, name='contribuicoes'),

	url(r'^login/$', views.login, name='login'),
	url(r'^valida-usuario/$', views.valida_usuario, name='valida-usuario'),
]