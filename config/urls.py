from django.contrib import admin
from django.urls import path
from app.views import (
    onboarding,
    onboarding_start,
    space_main,
    space_room,
    memory_main,
    mypage_main,
)
from django.urls import include

from spaces.views import (
    home_main, 
    space_create_step1, 
    space_create_step2, 
    space_create_step3, 
    home_join_room
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_main, name='home_main'),
    path('onboarding/',onboarding, name='onboarding'),
    path('onboarding/start/', onboarding_start, name='onboarding_start'),
    path('space/', space_main, name='space_main'),
    path('memory/', memory_main, name='memory_main'),
    path('mypage/', mypage_main, name='mypage_main'),
    path('home/create-room/1/', space_create_step1, name='home_create_room1'),
    path('home/create-room/2/', space_create_step2, name='home_create_room2'),
    path('home/create-room/3/', space_create_step3, name='home_create_room3'),
    path('home/join-room/', home_join_room, name='home_join_room'),
    path('space/', space_main, name='space_main'),
    path('space/room/', space_room, name='space_room'),
    path('accounts/', include('accounts.urls')),
]