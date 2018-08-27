# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from gallery.models import Media, ClipForm
from gallery.models import User
from django.http import HttpResponse, JsonResponse
from django.core import serializers as jsonserializer
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf


def index(request):
    video_list = Media.objects.all()
    context = {'video_list': video_list}
    return render(request, 'videos/index.html', context)


def login(request):
    c = {}
    c.update(csrf(request))
    return render(request, 'auth/login.html', c)


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/videos')
    else:
        return HttpResponseRedirect('/invalid')


def loggedin(request):
    return render_to_response('/auth/loggedin.html', {'full_name': request.user.login})


def invalid_login(request):
    return render(request, '/auth/invalid.html')


def logout(request):
    auth.logout()

    return render_to_response('/auth/logout.html', )


def detail(request, videoid):
    # if request.method == 'POST':
    #     form = ClipForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return
    # else:
    form = ClipForm()
    current_video = Media.objects.get(pk=videoid)
    context = {'video': current_video, 'form': form}
    return render(request, 'videos/details.html', context)


def all_media(request):
    all_media_objects = Media.objects.all()

    return HttpResponse(jsonserializer.serialize("json", all_media_objects))


def all_users(request):
    all_users_objects = User.objects.all()

    return HttpResponse(jsonserializer.serialize("json", all_users_objects))
