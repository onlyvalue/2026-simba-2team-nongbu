"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from app.views import onboarding
from app.views import home_main
from app.views import space_main
from app.views import memory_main
from app.views import mypage_main
from app.views import home_create_room1
from app.views import home_create_room2
from app.views import home_join_room
from app.views import login
from app.views import signup
from django.urls import include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_main, name='home_main'),
    path('onboarding/',onboarding, name='onboarding'),
    path('space/', space_main, name='space_main'),
    path('memory/', memory_main, name='memory_main'),
    path('mypage/', mypage_main, name='mypage_main'),
    path('home/create-room/1/', home_create_room1, name='home_create_room1'),
    path('home/create-room/2/', home_create_room2, name='home_create_room2'),
    path('home/join-room/', home_join_room, name='home_join_room'),
    path('accounts/', include('accounts.urls')),
]