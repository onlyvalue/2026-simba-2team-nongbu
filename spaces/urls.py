from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_main, name='home_main'),
    path('create/step1/', views.space_create_step1, name='home_create_room1'),
    path('create/step2/', views.space_create_step2, name='home_create_room2'),
    path('create/step3/', views.space_create_step3, name='home_create_room3'),
    path('join/', views.home_join_room, name='home_join_room'),
    
]