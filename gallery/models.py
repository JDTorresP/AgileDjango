# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.forms import ModelForm
from django.urls import reverse
from django.utils.datetime_safe import datetime


class Clip(models.Model):
    idClip = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    seg_initial = models.BigIntegerField()
    seg_final = models.BigIntegerField()


class ClipForm(ModelForm):
    class Meta:
        model = Clip
        fields = {'name', 'seg_initial', 'seg_final'}


class User(models.Model):
    idUser = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=500)
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    photoUrl = models.CharField(max_length=500)

    def __unicode__(self):
        return self.name


class Clip_Media(models.Model):
    media = models.ForeignKey('Media')
    clip = models.ForeignKey('Clip')
    user = models.ForeignKey('User')


class Category(models.Model):
    idCategory = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

MEDIA_TYPE = (
    ('V', 'Video'),
    ('A', 'Audio'),
)

class Media(models.Model):
    idMedia = models.AutoField(primary_key=True)
    mediaType = models.CharField(max_length=255, choices=MEDIA_TYPE, default='V')
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    author = models.CharField(max_length=255)
    created = models.DateField(default=datetime.now)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=500)
    clips = models.ManyToManyField(Clip, through=Clip_Media)
    category = models.ForeignKey(Category, null=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('details', args=[str(self.idMedia)])

    def get_yt_code(self):
        """Returns the ID code of a youtube video, """
        # ex: https: // www.youtube.com / watch?v = wIaowvCQG1M, return wIaowvCQG1M
        if "embed" not in self.url:
            return self.url.split('?v=')[1]
        else:
            return self.url[self.url.find("embed/")+6:self.url.find("embed/")+17]
