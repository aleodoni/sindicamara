# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-16 13:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Filiado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matricula', models.CharField(max_length=4, unique=True)),
                ('nome', models.CharField(max_length=200)),
                ('situacao_sindical', models.CharField(choices=[('A', 'ATIVO'), ('I', 'INATIVO')], max_length=1)),
                ('data_filiacao', models.DateField()),
                ('email', models.EmailField(max_length=254)),
                ('data_nascimento', models.DateField()),
                ('cpf', models.CharField(max_length=14)),
                ('rg', models.CharField(max_length=11)),
                ('estado_civil', models.CharField(choices=[('S', 'SOLTEIRO'), ('C', 'CASADO'), ('D', 'DIVORCIADO'), ('U', 'UNIÃO ESTÁVEL'), ('V', 'VIÚVO')], max_length=1)),
                ('endereco', models.CharField(max_length=300)),
                ('bairro', models.CharField(max_length=200)),
                ('cep', models.CharField(max_length=8)),
                ('telefone', models.CharField(max_length=9)),
                ('cidade', models.IntegerField()),
                ('cargo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastro.Cargo')),
            ],
        ),
        migrations.CreateModel(
            name='Ramal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ramal', models.CharField(max_length=4)),
                ('filiado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastro.Filiado')),
            ],
        ),
        migrations.CreateModel(
            name='Setor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='SituacaoFuncional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='filiado',
            name='setor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastro.Setor'),
        ),
        migrations.AddField(
            model_name='filiado',
            name='situacao_funcional',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastro.SituacaoFuncional'),
        ),
    ]