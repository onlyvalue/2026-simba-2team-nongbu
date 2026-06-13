from django.urls import path
from .views import *
from django.urls import include

app_name = "spaces"

urlpatterns = [
    path('', space_main, name='space_main'),
    path('create-room/1/', space_create_step1, name='home_create_room1'),
    path('create-room/2/', space_create_step2, name='home_create_room2'),
    path('create-room/3/', space_create_step3, name='home_create_room3'),
    path('join/', join_space, name='join_space'),
    path('room/<int:space_id>/', space_room, name='space_room'),
    path('room/<int:space_id>/star/', include('stars.urls')),
]