# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-15 04:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poketracker', '0002_auto_20180314_2048'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='evolvesFromName',
            field=models.CharField(default=b'', max_length=20),
        ),
    ]