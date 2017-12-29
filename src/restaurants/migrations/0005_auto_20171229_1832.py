# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-29 18:32
from __future__ import unicode_literals

from django.db import migrations, models
import restaurants.validators


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0004_restaurant_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='category',
            field=models.CharField(blank=True, max_length=120, null=True, validators=[restaurants.validators.validate_category]),
        ),
    ]