# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-15 05:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poketracker', '0003_pokemon_evolvesfromname'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='caught',
            field=models.BooleanField(default=False),
        ),
    ]
