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
from django.utils.dateparse import parse_date
from django import forms
from django.db import connection, transaction

import csv
import codecs
from io import StringIO
import re
import textwrap
from datetime import datetime
from decimal import Decimal
from time import strptime

from cadastro.models import Filiado, SituacaoFuncional, Setor, Cargo
from importa.models import Contribuicao


@login_required(login_url='/importa/loga/')
def contribuicoes(request):
	if request.method == 'POST':
		form = UploadContribuicoesForm(request.POST, request.FILES)
		if form.is_valid():
			handle_contribuicoes_file(request, request.FILES)
			return HttpResponseRedirect('/importa')
	else:
		form = UploadContribuicoesForm()
	return render(request, 'contribuicoes.html', {'form': form})


@login_required(login_url='/importa/loga/')
def cadastro(request):
	if request.method == 'POST':
		form = UploadCadastroForm(request.POST, request.FILES)
		if form.is_valid():
			print(request.FILES)
			handle_cadastro_files(request, request.FILES)
			return HttpResponseRedirect('/importa')
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
				return redirect('/loga/?next=' + next)
		else:
			messages.add_message(request, messages.ERROR, "Usuário ou senha incorretos.")
			return redirect('/loga/?next=' + next) 


@login_required(login_url='/importa/loga/')
def sair(request):
	logout(request)
	return HttpResponseRedirect('../loga/')


def handle_cadastro_files(request, arquivos):
	f_ativos = arquivos['arquivo_ativos']
	f_inativos = arquivos['arquivo_inativos']

	csvf_ativos = StringIO(f_ativos.read().decode())
	csvf_inativos = StringIO(f_inativos.read().decode())

	reader_ativos = csv.DictReader(csvf_ativos)
	reader_inativos = csv.DictReader(csvf_inativos)
	
	processa_ativos(request, reader_ativos)
	processa_inativos(request, reader_inativos)

def processa_ativos(request, reader):
	situacao = SituacaoFuncional.objects.get(pk=1) # EFETIVO
	setor = Setor.objects.get(pk=1) # TAQUIGRAFIA
	cargo = Cargo.objects.get(pk=1) # TAQUIGRAFA
	total_ativos = 0
	total_erros = 0;

	for row in reader:
		# aqui devemos procssar cada linha e inserir na tabela de filiados (model na app cadastro)
		if (row['Matricula'] and row['Nome']):
			filiado = Filiado()
			filiado.matricula = row['Matricula']
			filiado.nome = row['Nome']
			filiado.situacao_funcional = situacao
			filiado.situacao_sindical = 'A'
			filiado.data_filiacao = formata_data(row['Data de Filiação'])
			#filiado.data_filiacao = datetime.today()
			filiado.email = row['e-mail']
			filiado.data_nascimento = formata_data(row['Data de Nasc.'])
			#filiado.data_nascimento = datetime.today()
			filiado.cpf = re.sub("\D", "", row['CPF'])
			filiado.rg = re.sub("\D", "", row['RG'])
			filiado.estado_civil = 'C'
			filiado.endereco = row['Endereço']
			filiado.bairro = row['Bairro']
			filiado.cep = re.sub("\D", "", row['CEP'])[0:8]
			filiado.telefone = re.sub("\D", "", row['Telefone'])[0:8]
			filiado.setor = setor
			filiado.cargo = cargo
			filiado.estado = 18 # Paraná
			filiado.cidade = 2878 # Curitiba
			filiado.save()
			total_ativos = total_ativos + 1
		else:
			total_erros = total_erros + 1
			
	messages.add_message(request, messages.SUCCESS, "Filiados ativos adicionados : %03d" % (total_ativos))
	if total_erros > 0:
		messages.add_message(request, messages.ERROR, "Problemas encontrados no arquivo de ativos : %03d" % (total_erros))


def processa_inativos(request, reader):
	situacao = SituacaoFuncional.objects.get(pk=1) # EFETIVO
	setor = Setor.objects.get(pk=1) # TAQUIGRAFIA
	cargo = Cargo.objects.get(pk=1) # TAQUIGRAFA
	total_inativos = 0
	total_erros = 0;

	for row in reader:
		# aqui devemos procssar cada linha e inserir na tabela de filiados (model na app cadastro)
		if (row['Matricula'] and row['Nome']):
			if Filiado.objects.filter(matricula=row['Matricula']).exists():
				filiado = Filiado.objects.get(matricula=row['Matricula'])
				filiado.situacao_sindical = 'I'
				filiado.save()
			else:
				filiado = Filiado()
				filiado.matricula = row['Matricula']
				filiado.nome = row['Nome']
				filiado.situacao_funcional = situacao
				filiado.data_filiacao = formata_data(row['Data de Filiação'])
				filiado.email = row['e-mail']
				filiado.data_nascimento = formata_data(row['Data de Nasc.'])
				filiado.cpf = re.sub("\D", "", row['CPF'])
				filiado.rg = re.sub("\D", "", row['RG'])
				filiado.estado_civil = 'C'
				filiado.endereco = row['Endereço']
				filiado.bairro = row['Bairro']
				filiado.situacao_sindical = 'I'
				filiado.cep = re.sub("\D", "", row['CEP'])[0:8]
				filiado.telefone = re.sub("\D", "", row['Telefone'])[0:8]
				filiado.setor = setor
				filiado.cargo = cargo
				filiado.estado = 18 # Paraná
				filiado.cidade = 2878 # Curitiba
				filiado.save()
				total_inativos = total_inativos + 1
		else:
			total_erros = total_erros + 1
	messages.add_message(request, messages.SUCCESS, "Filiados inativos adicionados : %03d" % (total_inativos))
	if total_erros > 0:
		messages.add_message(request, messages.ERROR, "Problemas encontrados no arquivo de inativos : %03d" % (total_erros))


@transaction.atomic
def handle_contribuicoes_file(request, arquivos):
	array_data = request.POST.get('data').split("/")
	data = '01/' + array_data[1] + '/' + array_data[2]
	data_f = datetime.strptime(data, "%d/%m/%Y")
	f_cmc = arquivos['arquivo_cmc']
	f_ipmc = arquivos['arquivo_ipmc']

	txt_cmc = StringIO(f_cmc.read().decode("iso-8859-1"))
	txt_ipmc = StringIO(f_ipmc.read().decode("iso-8859-1"))

	seta_filiados_inativos()

	processa_cmc_and_ipmc(request, txt_cmc, 'CMC', data_f)
	processa_cmc_and_ipmc(request, txt_ipmc, 'IPMC', data_f)


def processa_cmc_and_ipmc(request, reader, tipo, data):
	total = 0
	total_erros = 0;
	reg = re.compile("\s{2}(\d{4})\s{5}")

	for row in reader:
		if (reg.findall(row)):
			matricula = (row[2:6])
			valor = Decimal(re.sub(r'[^\d.]', '', row[71:76]))
			if Filiado.objects.filter(matricula=int(matricula)).exists():
				filiado = Filiado.objects.get(matricula=int(matricula))
				filiado.situacao_sindical = 'A'
				filiado.save()
			contribuicao = Contribuicao()
			contribuicao.filiado = filiado
			contribuicao.valor = valor/100
			contribuicao.data = data
			contribuicao.save()
			total = total + 1
			
	messages.add_message(request, messages.SUCCESS, "Contribuições adicionadas %s : %03d" % (tipo, total))


def seta_filiados_inativos():
	cursor = connection.cursor()
	cursor.execute("UPDATE main.cadastro_filiado SET situacao_sindical='I'")
	#transaction.set_dirty()
	#transaction.commit()


def formata_data(data):
	try:
		retorno = datetime.strptime(data, "%d/%m/%Y")
		print(retorno.year)
	except Exception as e:
		retorno = None
	if retorno == None:
		try:
			retorno = datetime.strptime(data, "%d/%m/%y")
			if retorno.year > 2020:
				retorno = retorno.replace(year=retorno.year-100)
		except Exception as e:
			retorno = None
	return retorno