from django import forms

class UploadContribuicoesForm(forms.Form):
	data = forms.DateField()
	arquivo_ativos = forms.FileField()
	arquivo_inativos = forms.FileField()


class UploadCadastroForm(forms.Form):
	arquivo_ativos = forms.FileField()
	arquivo_inativos = forms.FileField()	