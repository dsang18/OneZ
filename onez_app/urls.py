"""onez URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name="home"),
    path('InstaDp/', views.HD_DP, name="insta_dp"),
    path('InstaReel/', views.insta_reel, name="insta_reel"),
    path('youtube_audio/', views.youtube_to_audio, name="youtube_to_mp3"),
    path('youtube_video/', views.youtube_to_video, name="youtube_to_mp4"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
