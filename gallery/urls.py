from django.conf.urls import url, include
from . import views
from django.contrib.auth.views import login

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^media/$', views.all_media, name="All media"),
    url(r'^users/$', views.all_users, name="All users"),
    url(r'^addUser/$', views.add_user_view, name='addUser'),
    url(r'^details/(?P<videoid>\d+)$', views.detail, name="details"),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
]

