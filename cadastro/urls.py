# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf.urls import patterns

from . import views
from importa.views import loga, valida_usuario, sair

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^filiado/novo$', views.FiliadoCreate.as_view(), name='filiado-novo'),
	url(r'^filiado/altera/(?P<pk>[0-9]+)/$', views.FiliadoUpdate.as_view(), name='altera'),
	url(r'^filiado/deleta/(?P<pk>[0-9]+)/$', views.FiliadoDeleta.as_view(), name='deleta'),
	url(r'^filiado/pesquisa$', views.FiliadoList.as_view(), name='filiado-pesquisa'),
	#url(r'^cadastro/$', views.cadastro, name='cadastro'),
	#url(r'^contribuicoes/$', views.contribuicoes, name='contribuicoes'),

	url(r'^loga/$', loga, name='loga'),
	url(r'^valida-usuario/$', valida_usuario, name='valida-usuario'),
	url(r'^sair/$', sair, name='sair'),
]