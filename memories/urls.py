from django.urls import path
from .views import *

app_name = 'memories'

urlpatterns = [
    path('', memory_main, name='memory_main'), 
    path('memory_gallery_list/', memory_gallery_list, name='memory_gallery_list'),
    path('gallery/', memory_gallery, name='memory_gallery'),
    path('<int:space_id>/constellation/', memory_constellation, name='memory_constellation'),
]

    