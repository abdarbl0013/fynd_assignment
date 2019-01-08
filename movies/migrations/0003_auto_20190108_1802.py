# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-01-08 18:02
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20190106_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='director',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='movie',
            name='popularity',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(99.0), django.core.validators.MinValueValidator(0)]),
        ),
    ]