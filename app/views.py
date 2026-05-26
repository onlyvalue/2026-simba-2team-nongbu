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

def home_create_room1(request):
    return render(request, 'home/home_create_room1.html')

def home_create_room2(request):
    return render(request, 'home/home_create_room2.html')

def home_join_room(request):
    return render(request, 'home/home_join_room.html')

def login(request):
    return render(request, 'auth/login.html')

def signup(request):
    return render(request, 'auth/signup.html')

def nickname_setup(request):
    return render(request, 'auth/nickname_setup.html')

def login(request):
    if request.method == "GET":
        return render(request, 'auth/login.html')
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = PracticeUser.objects.filter(
            username=username,
            password=password
        ).first()

        if user:
            return redirect('home_main')

        return render(request, 'auth/login.html', {
            'login_error': '아이디 또는 비밀번호가 올바르지 않습니다.'
        })