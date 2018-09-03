# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


from .models import Media, ClipForm, UserForm, EditUserForm, CustomUser, Category, EditCustomUserForm, Clip_Media

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, request
from django.shortcuts import render_to_response

from django.contrib import auth
from django.template.context_processors import csrf

from django.core import serializers as jsonserializer


def index(request):
    video_list = Media.objects.all()
    selected_category = 0
    selected_type = 0
    categoria_list = Category.objects.all().order_by('name')
    type_list = [{'idType':'1','name':'Videos'},{'idType':'2','name':'Audios'}]

    if request.method == 'POST':
        selected_category = int(request.POST.get("idSelCategorias",0))
        arg = request.POST.get("idSelTipo",0)
        selected_type =int(arg)
        if selected_category != 0:
            video_list = Media.objects.filter(category=selected_category)
        if selected_type != 0:
            if selected_type==1:
                video_list = Media.objects.filter(mediaType='V')
            else:
                if selected_type==2:
                    video_list = Media.objects.filter(mediaType='A')

    context = {'video_list': video_list, 'categoria_list': categoria_list, 'selected_category': selected_category, 'selected_type':selected_type,'type_list':type_list}
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
    if request.method == 'POST':
        form = ClipForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated():
                clip = form.save()
                video = Media.objects.get(pk=videoid)
                current_user = request.user
                media_clip = Clip_Media(clip= clip, media=video, user=current_user)
                media_clip.save()
        return HttpResponseRedirect(reverse('gallery:details', args=videoid))
    else:
        form = ClipForm()
        current_video = Media.objects.get(pk=videoid)
        context = {'video': current_video, 'form': form}
        return render(request, 'videos/details.html', context)

def detailSC(request, videoid):
    if request.method == 'POST':
        form = ClipForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated():
                clip = form.save()
                video = Media.objects.get(pk=videoid)
                current_user = request.user
                media_clip = Clip_Media(clip= clip, media=video, user=current_user)
                media_clip.save()
        return HttpResponseRedirect(reverse('gallery:detailsSC', args=videoid))
    else:
        form = ClipForm()
        current_video = Media.objects.get(pk=videoid)
        context = {'video': current_video, 'form': form}
        return render(request, 'videos/detailsSC.html', context)

def all_media(request):
    all_media_objects = Media.objects.all()

    return HttpResponse(jsonserializer.serialize("json", all_media_objects))


def all_users(request):
    all_users_objects = User.objects.all()

    return HttpResponse(jsonserializer.serialize("json", all_users_objects))


def add_user_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            username = cleaned_data.get('usuario')
            first_name = cleaned_data.get('nombre')
            last_name = cleaned_data.get('apellido')
            password = cleaned_data.get('contrasena')
            email = cleaned_data.get('email')

            user_model = User.objects.create_user(username=username, password=password)
            user_model.first_name = first_name
            user_model.last_name = last_name
            user_model.email = email

            user_app = CustomUser(pais=cleaned_data.get('pais'),
                                  ciudad=cleaned_data.get('ciudad'),
                                  imagen=cleaned_data.get('imagen'),
                                  auth_user_id=user_model)

            user_model.save()
            user_app.save()
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
        user = User.objects.get(username=request.user.username)
        customuser = CustomUser.objects.filter(auth_user_id=user).first()
        customform = EditCustomUserForm(request.POST, request.FILES, instance=customuser)

        if form.is_valid():
            if customform.is_valid():
                form.save()
                customform.save()
                return HttpResponseRedirect(reverse('gallery:index'))

    else:
        user = User.objects.get(username=request.user.username)
        print('username ' + user.username)
        form = EditUserForm(instance=user)
        customuser = CustomUser.objects.filter(auth_user_id=user).first()
        customform = EditCustomUserForm(instance=customuser)

    context = {
        'form': form,
        'customform': customform
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
