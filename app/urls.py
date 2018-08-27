"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from app import settings
from django.contrib.auth.views import login
from gallery import views


urlpatterns = [
    url(r'^login/$', login,  {'template_name':'auth/login.html'}),
    url(r'^login/accounts/auth/$', views.auth_view, name="auth_view"),
    url(r'^videos/', include('gallery.urls'),name='videos_url'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/gallery/', include('gallery.urls', namespace='gallery')),
<<<<<<< HEAD
    url(r'^invalid/$',views.invalid_login,name='invalid'),
=======
    url(r'^$', include('gallery.urls', namespace='gallery'))
>>>>>>> 0c3203f5d687057dd5e44c81e617d1810bd77473
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)