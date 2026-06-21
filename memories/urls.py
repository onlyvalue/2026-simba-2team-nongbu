from django.urls import path
from .views import *

app_name = 'memories'

urlpatterns = [
    path('', memory_main, name='memory_main'), 
    path('calender/<int:space_id>', memory_gallery_list, name='memory_gallery_list'),
    path('gallery/<int:space_id>', memory_gallery, name='memory_gallery'),
    path('constellation/<int:space_id>', memory_constellation, name='memory_constellation'),
]  