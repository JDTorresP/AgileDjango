# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-20 02:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='photoUrl',
            field=models.CharField(default='http://photo.com', max_length=500),
            preserve_default=False,
        ),
    ]
