# Generated by Django 2.0.4 on 2018-04-19 19:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('candies_to_evolve', models.IntegerField(default=0)),
                ('caught', models.BooleanField(default=False)),
                ('num_in_bag', models.IntegerField(default=0)),
                ('base_evolution', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='base_evolution2', to='pokemon.Pokemon')),
                ('evolves_from', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='evolves_from2', to='pokemon.Pokemon')),
            ],
        ),
    ]
