# -*- coding: utf-8 -*-

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

@login_required(login_url='/importa/loga/')
def contribuicoes(request):
	if request.method == 'POST':
		form = UploadContribuicoesForm(request.POST, request.FILES)
		if form.is_valid():
			handle_uploaded_file(request.FILES['file'])
			return HttpResponseRedirect('/success/url/')
	else:
		form = UploadContribuicoesForm()
	return render(request, 'contribuicoes.html', {'form': form})


@login_required(login_url='/importa/loga/')
def cadastro(request):
	if request.method == 'POST':
		form = UploadCadastroForm(request.POST, request.FILES)
		if form.is_valid():
			handle_uploaded_file(request.FILES['file'])
			return HttpResponseRedirect('/success/url/')
	else:
		form = UploadCadastroForm()
	return render(request, 'cadastro.html', {'form': form})	


@login_required(login_url='/importa/loga/')
def index(request):
	return render_to_response('index.html', context_instance=RequestContext(request))	


def loga(request):
	next = request.GET.get('next')
	return render_to_response('login.html', RequestContext(request, {'next': next}))	


def valida_usuario(request):
	if request.method == 'POST':
		usuario = request.POST.get('usuario')
		senha = request.POST.get('senha')
		next = request.POST.get('next')
		user = authenticate(username=usuario, password=senha)
		if user is not None:
			if user.is_active:
				login(request, user)
				if next != None and next != 'None':
					return HttpResponseRedirect(next)
				return render_to_response('index.html', context_instance=RequestContext(request))
			else:
				messages.add_message(request, messages.ERROR, "Usuário válido mas desebilitado.")
				return redirect('/importa/loga/?next=' + next)
		else:
			messages.add_message(request, messages.ERROR, "Usuário ou senha incorretos.")
			return redirect('/importa/loga/?next=' + next) 


@login_required(login_url='/importa/loga/')
def sair(request):
	logout(request)
	return HttpResponseRedirect('/importa/loga/')			