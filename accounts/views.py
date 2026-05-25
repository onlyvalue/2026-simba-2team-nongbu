from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import render, redirect
from .models import Profile

def signup(request):
    
    if request.method == "POST":

        if User.objects.filter(username=request.POST['username']).exists():
            return render(request, "auth/signup.html", {'error': '이미 존재하는 아이디입니다.'})
        
        if request.POST['password'] == request.POST['password_confirm']:
            new_user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password'],
            )

            profile = new_user.profile
            profile.nickname = request.POST['nickname']
            profile.save()

            auth.login(request, new_user)
            return redirect("home_main")
        else:
            return render(request, "auth/signup.html", {'error': '비밀번호가 일치하지 않습니다.'})
        
    return render(request, "auth/signup.html")

def login(request): 
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("home_main")
        else:
            return render(request, "auth/login.html",{'error': '아이디 또는 비밀번호가 일치하지 않습니다.'})
        
    elif request.method == "GET":
        return render(request, "auth/login.html")

def logout(request):
    auth.logout(request)
    return redirect("onboarding")