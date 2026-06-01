from django.shortcuts import render, redirect
from .models import PracticeUser

def home_main(request):
    return render(request, 'home/home_main.html')

def space_main(request):
    return render(request, 'space/space_main.html')

def memory_main(request):
    return render(request, 'memory/memory_main.html')

def mypage_main(request):
    return render(request, 'mypage/mypage_main.html')

def onboarding(request):
    return render(request, 'onboarding/onboarding.html')

def onboarding_start(request):
    return render(request, 'onboarding/onboarding_start.html')

def nickname_setup(request):
    return render(request, 'auth/nickname_setup.html')

def home_create_room1(request):
    return render(request, 'home/home_create_room1.html')

def home_create_room2(request):
    return render(request, 'home/home_create_room2.html')

def home_create_room3(request):
    return render(request, 'home/home_create_room3.html')

def home_join_room(request):
    return render(request, 'home/home_join_room.html')