# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.db.models import Sum
from smart_selects.db_fields import ChainedForeignKey

@python_2_unicode_compatible
class Associado(models.Model):
	matricula = models.CharField(max_length=4, unique=True)
	nome = models.CharField(max_length=200)
	tipo = models.CharField(max_length=10)
	situacao = models.CharField(max_length=1, default='A')

	def __str__(self):
		return self.nome

@python_2_unicode_compatible
class Contribuicao(models.Model):
	associado = models.ForeignKey('Associado')
	data = models.DateField()
	valor = models.DecimalField(max_digits=8, decimal_places=2)

	def __str__(self):
		return self.associado.matricula + ' - ' + data.strftime('%m/%y')