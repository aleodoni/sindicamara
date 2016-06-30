# -*- coding: utf-8 -*-

from django.forms import ModelForm, CharField, DecimalField, DateField, BooleanField
from django.forms.models import inlineformset_factory
from django.forms import formsets, models
from django.forms.models import modelformset_factory
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div, Button, HTML, ButtonHolder
from crispy_forms.bootstrap import (PrependedText, PrependedAppendedText, FormActions, AppendedText)
from crispy_forms.bootstrap import StrictButton
from django.conf import settings
from decimal import Decimal
from django import forms

from datetime import datetime

from .models import SituacaoFuncional, SITUACAO_SINDICAL, ESTADO_CIVIL, Filiado, Cargo, Setor

class FiliadoPesquisa(forms.Form):

	matricula = forms.CharField(label='Matrícula', required=False)
	nome = forms.CharField(label='Nome', required=False)
	situacao_funcional = forms.ModelChoiceField(label='Situação Funcional', queryset=SituacaoFuncional.objects.all(), required=False)
	situacao_sindical = forms.ChoiceField(label='Situação Sindical', choices=SITUACAO_SINDICAL, required=False)

	def __init__(self, *args, **kwargs):
		super(FiliadoPesquisa, self).__init__(*args, **kwargs)

		self.helper = FormHelper()
		self.helper.form_tag = False
		self.helper.layout = Layout(
			Div(
				Div('matricula', css_class='col-md-2',),
				Div('nome', css_class='col-md-10',),
				css_class='col-md-12 row',
			),
			Div(
				Div('situacao_funcional', css_class='col-md-6',),
				Div('situacao_sindical', css_class='col-md-6',),
				css_class='col-md-12 row',
			),
			Div(
				Div(
					StrictButton('Pesquisar', css_class="btn-primary btn", id='btn_search', onclick='pesquisa()'),
					StrictButton('Imprimir', css_class="btn-default btn", id='btn_print', onclick='imprime()'),
					StrictButton('Incluir Filiado', css_class="btn-default btn", id='btn_new', onclick='novo()'),
					css_class='col-xs-12',
				),
				css_class='col-xs-12 row',
			),
		)


class FiliadoForm(ModelForm):
	matricula = forms.CharField(label='Matrícula')
	nome = forms.CharField(label='Nome')
	situacao_funcional = forms.ModelChoiceField(label='Situação Funcional', queryset=SituacaoFuncional.objects.all())
	situacao_sindical = forms.ChoiceField(label='Situação Sindical', choices=SITUACAO_SINDICAL)
	data_filiacao = forms.DateField(label='Data de Filiação', required=False)
	email = forms.EmailField(label='email', required=False)
	data_nascimento = forms.DateField(label='Data de Nascimento', required=False)
	cpf = forms.CharField(label='CPF', required=False)
	rg = forms.CharField(label='RG', required=False)
	estado_civil = forms.ChoiceField(label='Estado Civil', choices=ESTADO_CIVIL, required=False)
	endereco = forms.CharField(label='Endereço', required=False)
	bairro = forms.CharField(label='Bairro', required=False)
	cep = forms.CharField(label="CEP", required=False)
	telefone = forms.CharField(label='Telefone', required=False)
	setor = forms.ModelChoiceField(label='Setor', queryset=Setor.objects.all().order_by('nome'))
	cargo = forms.ModelChoiceField(label='Cargo', queryset=Cargo.objects.all().order_by('nome'))
	cidade = forms.IntegerField(required=False)
	estado = forms.IntegerField(required=False)

	class Meta:
		model = Filiado
		exclude = ['']

	def __init__(self, *args, **kwargs):
		super(FiliadoForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper()
		self.helper.form_tag = False
		self.helper.layout = Layout(
			Div(
				Div('matricula', css_class='col-md-2',),
				Div('nome', css_class='col-md-10',),
				css_class='col-md-12 row',
			),
			Div(
				Div('setor', css_class='col-md-6',),
				Div('cargo', css_class='col-md-6',),
				css_class='col-md-12 row',
			),
			Div(
				Div('situacao_funcional', css_class='col-md-6',),
				Div('situacao_sindical', css_class='col-md-6',),
				css_class='col-md-12 row',
			),
			Div(
				Div(AppendedText('data_filiacao', '<span class="glyphicon glyphicon-calendar"></span>'), css_class='col-md-4',),
				Div('estado_civil', css_class='col-md-4',),
				Div('email', css_class='col-md-4',),
				css_class='col-md-12 row',
			),
			Div(
				Div('cpf', css_class='col-md-6',),
				Div('rg', css_class='col-md-6',),
				css_class='col-md-12 row',
			),
			Div(
				Div('endereco', css_class='col-md-12',),
				css_class='col-md-12 row',
			),
			Div(
				Div('bairro', css_class='col-md-4',),
				Div('cep', css_class='col-md-4',),
				Div('telefone', css_class='col-md-4',),
				css_class='col-md-12 row',
			),
		)


class UploadContribuicoesForm(forms.Form):
	data = forms.DateField()
	arquivo_cmc = forms.FileField()
	arquivo_ipmc = forms.FileField()

	def __init__(self, *args, **kwargs):
		super(UploadContribuicoesForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_tag = False
		self.helper.layout = Layout(
			Div(
				Div(AppendedText('data', '<span class="glyphicon glyphicon-calendar"></span>'), css_class='col-md-6',),
				css_class='col-md-12 row',
			),
			Div(
				Div('arquivo_cmc', css_class='col-md-6',),
				Div('arquivo_ipmc', css_class='col-md-6',),
				css_class='col-md-12 row',
			),
			Div(
				Div(FormActions(Submit('save', 'Importar')), css_class='col-md-6',),
				css_class='col-md-12 row',
			),
		)

	def clean_data(self):
		data = self.cleaned_data['data']
		array_data = datetime.strftime(data, "%d/%m/%Y").split("/")
		str_data = '01/' + array_data[1] + '/' + array_data[2]
		data_f = datetime.strptime(str_data, "%d/%m/%Y")

		if Contribuicao.objects.filter(data=data_f).exists():
			raise forms.ValidationError("Já foi importado a contribuição de %s/%s" % (array_data[1], array_data[2]))
		return data


class UploadCadastroForm(forms.Form):
	arquivo_ativos = forms.FileField()
	arquivo_inativos = forms.FileField()	

	def __init__(self, *args, **kwargs):
		super(UploadCadastroForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.form_tag = False
		self.helper.layout = Layout(
			Div(
				Div('arquivo_ativos', css_class='col-md-6 file',),
				Div('arquivo_inativos', css_class='col-md-6',),
				css_class='col-md-12 row',
			),
			Div(
				Div(FormActions(Submit('save', 'Importar')), css_class='col-md-6',),
				css_class='col-md-12 row',
			),
		)