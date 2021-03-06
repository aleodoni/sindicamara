# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-16 17:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0002_auto_20160616_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filiado',
            name='bairro',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='filiado',
            name='cargo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cadastro.Cargo'),
        ),
        migrations.AlterField(
            model_name='filiado',
            name='cep',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='filiado',
            name='cidade',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='filiado',
            name='cpf',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
        migrations.AlterField(
            model_name='filiado',
            name='data_filiacao',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='filiado',
            name='data_nascimento',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='filiado',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='filiado',
            name='endereco',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='filiado',
            name='estado_civil',
            field=models.CharField(blank=True, choices=[('S', 'SOLTEIRO'), ('C', 'CASADO'), ('D', 'DIVORCIADO'), ('U', 'UNIÃO ESTÁVEL'), ('V', 'VIÚVO')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='filiado',
            name='rg',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
        migrations.AlterField(
            model_name='filiado',
            name='setor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cadastro.Setor'),
        ),
        migrations.AlterField(
            model_name='filiado',
            name='telefone',
            field=models.CharField(blank=True, max_length=9, null=True),
        ),
    ]
