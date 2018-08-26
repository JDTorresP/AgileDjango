# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from gallery.models import Media, ClipForm
from gallery.models import User
from django.http import HttpResponse, JsonResponse
from django.core import serializers as jsonserializer
from django.shortcuts import render


def index(request):
    video_list = Media.objects.all()
    context = {'video_list': video_list}
    return render(request, 'videos/index.html', context)

def detail(request, videoid):
    # if request.method == 'POST':
    #     form = ClipForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return
    # else:
    form = ClipForm()
    current_video = Media.objects.get(pk=videoid)
    context = {'video': current_video, 'form':form}
    return render(request, 'videos/details.html', context)


def all_media(request):
    all_media_objects = Media.objects.all()

    return HttpResponse(jsonserializer.serialize("json", all_media_objects))

def all_users(request):
    all_users_objects = User.objects.all()

    return HttpResponse(jsonserializer.serialize("json", all_users_objects))
