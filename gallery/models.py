# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import forms
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.urls import reverse
from django import forms
from django.utils.datetime_safe import datetime


class UserForm(ModelForm):
    username = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise forms.ValidationError('Nombre de usuario ya registrado.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError('Ya existe un email igual registrado.')
        return email

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Las claves no coinciden')
        return password2

    def __unicode__(self):
        return self.name


class Category(models.Model):
    idCategory = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Clip(models.Model):
    idClip = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    seg_initial = models.BigIntegerField()
    seg_final = models.BigIntegerField()


class ClipForm(ModelForm):
    class Meta:
        model = Clip
        fields = {'name', 'seg_initial', 'seg_final'}


class Clip_Media(models.Model):
    clip = models.ForeignKey('Clip')
    media = models.ForeignKey('Media')
    user = models.ForeignKey(User)


class Media(models.Model):
    idMedia = models.AutoField(primary_key=True)
    mediaType = models.CharField(max_length=255)
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







