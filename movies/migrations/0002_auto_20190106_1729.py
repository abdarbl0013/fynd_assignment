# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-01-06 17:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='imdb_rating',
            new_name='imdb_score',
        ),
    ]
