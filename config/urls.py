from django.contrib import admin
from django.urls import path
from app.views import onboarding
from app.views import onboarding_start
from app.views import home_main
from app.views import space_main
from app.views import memory_main
from app.views import mypage_main
from app.views import home_create_room1
from app.views import home_create_room2
from app.views import home_create_room3
from app.views import home_join_room
from django.urls import include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_main, name='home_main'),
    path('onboarding/',onboarding, name='onboarding'),
    path('onboarding/start/', onboarding_start, name='onboarding_start'),
    path('space/', space_main, name='space_main'),
    path('memory/', memory_main, name='memory_main'),
    path('mypage/', mypage_main, name='mypage_main'),
    path('home/create-room/1/', home_create_room1, name='home_create_room1'),
    path('home/create-room/2/', home_create_room2, name='home_create_room2'),
    path('home/create-room/3/', home_create_room3, name='home_create_room3'),
    path('home/join-room/', home_join_room, name='home_join_room'),
    path('accounts/', include('accounts.urls')),
]