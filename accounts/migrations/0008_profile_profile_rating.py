# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-17 11:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20171015_1313'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_rating',
            field=models.FloatField(default=0.0),
        ),
    ]
