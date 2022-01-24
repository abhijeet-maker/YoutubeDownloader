"""YoutubeDL URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import *
from django.views.static import serve
from VidDl import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index, name="index"),
    path('', views.index),
    path('home/', views.home, name="home"),
    path('get_resolution/', views.get_videos_res),
    #Downloaded on local server
    path('download/', views.select_videos_res),
    #serve over client now
    path('download_completed/', views.download),
#path('download_completed/', views.download_completed),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)