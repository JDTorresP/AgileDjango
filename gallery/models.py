# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Clip(models.Model):
    idClip = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    seg_initial = models.BigIntegerField()
    seg_final = models.BigIntegerField()


class User(models.Model):
    idUser = models.FloatField(primary_key=True)
    name = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=500)
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)


class Media(models.Model):
    idMedia = models.FloatField(primary_key=True)
    mediaType = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    author = models.CharField(max_length=255)
    created = models.BigIntegerField()
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=500)
    clips = models.ManyToManyField(Clip)
