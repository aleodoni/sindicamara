# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.db.models import Sum
from smart_selects.db_fields import ChainedForeignKey

SITUACAO_SINDICAL = (
    ('A', 'ATIVO'),
    ('I', 'INATIVO'),
)

ESTADO_CIVIL = (
    ('S', 'SOLTEIRO'),
    ('C', 'CASADO'),
    ('D', 'DIVORCIADO'),
    ('U', 'UNIÃO ESTÁVEL'),
    ('V', 'VIÚVO'),
)

@python_2_unicode_compatible
class Filiado(models.Model):
	matricula = models.CharField(max_length=4, unique=True)
	nome = models.CharField(max_length=200)
	situacao_funcional = models.ForeignKey('SituacaoFuncional')
	situacao_sindical = models.CharField(max_length=1, choices=SITUACAO_SINDICAL)
	data_filiacao = models.DateField(blank=True, null=True)
	email = models.EmailField(blank=True, null=True)
	data_nascimento = models.DateField(blank=True, null=True)
	cpf = models.CharField(max_length=14, blank=True, null=True)
	rg = models.CharField(max_length=11, blank=True, null=True)
	estado_civil = models.CharField(max_length=1, choices=ESTADO_CIVIL, blank=True, null=True)
	endereco = models.CharField(max_length=300, blank=True, null=True)
	bairro = models.CharField(max_length=200, blank=True, null=True)
	cep = models.CharField(max_length=8, blank=True, null=True)
	telefone = models.CharField(max_length=9, blank=True, null=True)
	setor = models.ForeignKey('Setor', blank=True, null=True)
	cargo = models.ForeignKey('Cargo', blank=True, null=True)
	cidade = models.IntegerField(blank=True, null=True)

	def __str__(self):
		return self.nome


@python_2_unicode_compatible
class SituacaoFuncional(models.Model):
	nome = models.CharField(max_length=200)

	def __str__(self):
		return self.nome


@python_2_unicode_compatible
class Setor(models.Model):
	nome = models.CharField(max_length=200)

	def __str__(self):
		return self.nome


@python_2_unicode_compatible
class Cargo(models.Model):
	nome = models.CharField(max_length=200)

	def __str__(self):
		return self.nome


@python_2_unicode_compatible
class Ramal(models.Model):
	ramal = models.CharField(max_length=4)
	filiado = models.ForeignKey('Filiado', on_delete=models.CASCADE)

	def __str__(self):
		return self.ramal		