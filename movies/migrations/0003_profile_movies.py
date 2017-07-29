# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-06 14:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20170106_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='movies',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users_watched', to='movies.Movie'),
        ),
    ]