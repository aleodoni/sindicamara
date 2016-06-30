# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.db.models import Sum
from smart_selects.db_fields import ChainedForeignKey
from cadastro.models import Filiado

@python_2_unicode_compatible
class Contribuicao(models.Model):
	filiado = models.ForeignKey('cadastro.Filiado')
	data = models.DateField()
	valor = models.DecimalField(max_digits=8, decimal_places=2)

	def __str__(self):
		return self.filiado.matricula + ' - ' + data.strftime('%m/%y')
