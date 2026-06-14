from django.contrib import admin
from django.urls import path
from app.views import (
    onboarding,
    onboarding_start,
    space_room,
    space_upload,
    memory_main,
    mypage_main,
)
from django.urls import include

from spaces.views import home_main




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_main, name='home_main'),
    path('onboarding/',onboarding, name='onboarding'),
    path('onboarding/start/', onboarding_start, name='onboarding_start'),
    path('mypage/', mypage_main, name='mypage_main'),
    path('space/', include('spaces.urls')),
    path('account/', include('accounts.urls')),
    path('memory/', include('memories.urls')),
    path('space/upload/', space_upload, name='space_upload'),
]