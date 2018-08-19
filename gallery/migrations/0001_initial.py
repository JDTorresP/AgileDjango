# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-19 23:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('idCategory', models.FloatField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Clip',
            fields=[
                ('idClip', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('seg_initial', models.BigIntegerField()),
                ('seg_final', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Clip_Media',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gallery.Clip')),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('idMedia', models.FloatField(primary_key=True, serialize=False)),
                ('mediaType', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=500)),
                ('author', models.CharField(max_length=255)),
                ('created', models.BigIntegerField()),
                ('country', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=500)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gallery.Category')),
                ('clips', models.ManyToManyField(through='gallery.Clip_Media', to='gallery.Clip')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('idUser', models.FloatField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('lastName', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=500)),
                ('login', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='media',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gallery.User'),
        ),
        migrations.AddField(
            model_name='clip_media',
            name='media',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gallery.Media'),
        ),
        migrations.AddField(
            model_name='clip_media',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gallery.User'),
        ),
    ]
