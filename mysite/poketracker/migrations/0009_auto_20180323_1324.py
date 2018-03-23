# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-23 20:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poketracker', '0008_auto_20180323_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='evolvesFrom',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='poketracker.Pokemon'),
        ),
    ]
