from django.urls import path
from .views import *

app_name = "accounts"

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('signup/', signup, name='signup'),
    path('nickname_setup/', nickname_setup, name='nickname_setup'),
    path('change_password/', change_password, name='change_password'),
    path('delete_account/', delete_account, name='delete_account'),
    path('change_nickname/', change_nickname, name='change_nickname')
]