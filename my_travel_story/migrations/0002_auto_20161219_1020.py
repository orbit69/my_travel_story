# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-19 10:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_travel_story', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='photo',
            field=models.ImageField(blank=True, upload_to='my_travel_story/static/place_images'),
        ),
    ]
