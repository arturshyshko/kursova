# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-12 16:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0007_auto_20170106_1733'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together=set([]),
        ),
    ]