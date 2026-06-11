from django.urls import path
from .views import *

app_name = "spaces"

urlpatterns = [
    path('', space_main, name='space_main'),
    path('create-room/1/', space_create_step1, name='home_create_room1'),
    path('create-room/2/', space_create_step2, name='home_create_room2'),
    path('create-room/3/', space_create_step3, name='home_create_room3'),
    path('join/', home_join_room, name='home_join_room'),
    path('room/', space_room, name='space_room'),
]