from django.urls import path
from .views import *

app_name = 'memories'

urlpatterns = [
    path('', memory_main, name='memory_main'), 
]