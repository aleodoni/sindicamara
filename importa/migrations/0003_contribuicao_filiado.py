# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-16 13:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0001_initial'),
        ('importa', '0002_auto_20160616_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='contribuicao',
            name='filiado',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='cadastro.Filiado'),
            preserve_default=False,
        ),
    ]
