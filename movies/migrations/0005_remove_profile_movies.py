# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-06 15:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_auto_20170106_1502'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='movies',
        ),
    ]
