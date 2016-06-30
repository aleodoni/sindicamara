# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from .forms import UploadCadastroForm, UploadContribuicoesForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.html import format_html
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
from django import forms
from django.db import connection, transaction
from django.contrib.messages.views import SuccessMessageMixin

from .forms import FiliadoPesquisa, FiliadoForm
from sindicamara.classes import seguranca
from .models import Filiado


@login_required(login_url='/cadastro/loga/')
def index(request):
	return render_to_response('index.html', context_instance=RequestContext(request))	


class FiliadoList(seguranca.SindicamaraLoginRequired, FormView):
	template_name = "cadastro/search.html"
	form_class = FiliadoPesquisa
	success_url = '/cadastro/filiado/pesquisa'

	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		context['form'] = FiliadoPesquisa(request.GET)
		#monta a query baseada nos argumentos do request e coloca o resultado no contexto
		matricula = request.GET.get('matricula', None)
		nome = request.GET.get('nome', None)
		situacao_funcional = request.GET.get('situacao_funcional', None)
		situacao_sindical = request.GET.get('situacao_sindical', 'A')
		filiados = Filiado.objects.all()

		if matricula is not None and matricula != '':
			filiados = Filiado.objects.filter(matricula=matricula)
		if nome is not None and nome != '':
			filiados = filiados.filter(nome__icontains=nome)
		if situacao_sindical is not None and situacao_sindical != '':
			filiados = filiados.filter(situacao_sindical=situacao_sindical)
		if situacao_funcional is not None and situacao_funcional != '':
			filiados = filiados.filter(situacao_funcional=situacao_funcional)
		context['filiados'] = filiados
		return self.render_to_response(context)


class FiliadoCreate(seguranca.SindicamaraLoginRequired, SuccessMessageMixin, CreateView):
	template_name = "cadastro/new.html"
	form_class = FiliadoForm
	model = Filiado
	success_url = '/cadastro/filiado/pesquisa'
	success_message = "Filiado criado com sucesso"


class FiliadoUpdate(seguranca.SindicamaraLoginRequired, SuccessMessageMixin, UpdateView):
	template_name = "cadastro/update.html"
	form_class = FiliadoForm	
	model = Filiado
	success_url = '/cadastro/filiado/pesquisa'
	success_message = "Filiado atualizado com sucesso"


class FiliadoDeleta(seguranca.SindicamaraLoginRequired, SuccessMessageMixin, DeleteView):
	model = Filiado
	template_name = "cadastro/deleta.html"
	success_url = '/cadastro/filiado/pesquisa'
	success_message = "Filiado excluído com sucesso"	