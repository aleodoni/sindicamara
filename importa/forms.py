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

from .models import Contribuicao

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