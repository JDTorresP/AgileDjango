# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Media, ClipForm, UserForm, EditUserForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, request
from django.shortcuts import render_to_response

from django.contrib import auth
from django.template.context_processors import csrf

from django.core import serializers as jsonserializer


def index(request):
    video_list = Media.objects.all()
    context = {'video_list': video_list}
    return render(request, 'videos/index.html', context)


# def login(request):
#     c = {}
#     c.update(csrf(request))
#     return render(request, 'auth/login.html', c)


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/videos')
    else:
        return HttpResponseRedirect('/invalid')


# def loggedin(request):
#     return render_to_response('/auth/loggedin.html', {'full_name': request.user.login})


# def invalid_login(request):
#     return render(request, '/auth/invalid.html')
#
#
# def logout(request):
#     auth.logout()
#
#     return render_to_response('/auth/logout.html', )
#

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


def add_user_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            username = cleaned_data.get('username')
            first_name = cleaned_data.get('first_name')
            last_name = cleaned_data.get('last_name')
            password = cleaned_data.get('password')
            email = cleaned_data.get('email')

            user_model = User.objects.create_user(username=username, password=password)
            user_model.first_name = first_name
            user_model.last_name = last_name
            user_model.email = email
            user_model.save()

            return HttpResponseRedirect(reverse('gallery:index'))

    else:
        form = UserForm()

    context = {
        'form': form
    }

    return render(request, 'auth/registro.html', context)


def mod_user_view(request):
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('gallery:index'))

    else:
        print('else?')
        user = User.objects.get(username=request.user.username)
        form = EditUserForm(instance=user)

    context = {
        'form': form
    }

    return render(request, 'auth/modUser.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user=form.user)
            return HttpResponseRedirect(reverse('gallery:index'))
    else:
        form = PasswordChangeForm(user=request.user)
    context = {
        'form': form
    }
    return render(request, 'auth/changePassword.html', context)


def login_view(request):

    if request.user.is_authenticated():
        return redirect(reverse('gallery:index'))

    mensaje = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('gallery:index'))
        else:
            mensaje = "Nombre de usuario o clave no valido"

    return render(request, 'auth/login.html', {'mensaje': mensaje})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('gallery:index'))
