# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-06 13:58
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='globalRate', to='movies.Movie')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='globalrating',
            unique_together=set([('movie', 'position')]),
        ),
    ]
