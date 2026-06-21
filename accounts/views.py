from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib import auth
from django.shortcuts import render, redirect
from .models import Profile
import re

def signup(request):
    
    if request.method == "POST":    
        # 무슨 버튼 눌렀는지 확인
        check_action = request.POST.get('check_action')
        # 아이디 비밀번호 비밀번호 확인 가져오기 
        username = request.POST.get('username').strip()
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
    
        # 아이디
        if check_action == "check_username": 
            # 정규표현식으로 아이디 유효성 검사
            if not re.match(r'^[a-z][a-z0-9]{3,11}$', username):
                return render(request, "auth/signup.html", {'username_error': '영문 소문자와 숫자만 사용하여, 영문 소문자로 시작하는 4~12자의\n아이디를 입력해주세요' , 'username': username})

            # 아이디 중복 여부 검사
            if User.objects.filter(username=username).exists(): 
                return render(request, "auth/signup.html", {'username_duplicate_error': '이미 존재하는 아이디입니다', 'username': username})
            
            # 중복검사 통과하면 아이디 저장
            else:
                request.session['checked_username'] = username 
                return render(request, "auth/signup.html", {'username_success': '사용 가능한 아이디입니다', 'username': username})

        # 비밀번호
        elif check_action == "signup": 
            # 중복검사 통과한 아이디인지 확인
            if request.session.get('checked_username') != username: 
                return render(request, "auth/signup.html", {'error_ischeck': '아이디 중복검사를 먼저 진행해주세요', 'username': username})
            
            # 정규표현식으로 비밀번호 유효성 검사
            if len(password) < 8 or not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password) or re.search(r"\s", password): 
                return render(request, "auth/signup.html", {'password_error': '8자리 이상, 특수문자를 포함한 비밀번호를 입력해주세요', 'username': username, 'username_success': '사용 가능한 아이디입니다'})

            # 비밀번호 일치 여부 검사
            if password != password_confirm: 
                return render(request, "auth/signup.html", {'password_confirm_error': '비밀번호가 일치하지 않습니다', 'username': username, 'username_success': '사용 가능한 아이디입니다'})
        
            
            # 모든 검사 통과 시 회원가입 진행
            new_user = User.objects.create_user(
                username=username,
                password=password,
            )

            # 아이디 중복검사 초기화
            request.session['checked_username'] = ''    

            auth.login(request, new_user)
            return redirect("accounts:nickname_setup")
    
    return render(request, "auth/signup.html")

def login(request): 
    if request.method == "POST":
        # 아이디와 비밀번호 가져오기
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 아이디와 비밀번호가 일치하는지 확인
        user = auth.authenticate(request, username=username, password=password) 
        if user is not None:
            auth.login(request, user)
            return redirect("home_main")
        else:
            return render(request, "auth/login.html", {'error': '아이디 또는 비밀번호가 일치하지 않습니다.'})
        
    return render(request, "auth/login.html")

def logout(request):
    auth.logout(request)
    return redirect("onboarding")

def nickname_setup(request):
    # 로그인 여부 확인
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.method == "POST":
        # 닉네임 가져오기
        nickname = request.POST.get('nickname').strip()

        # 닉네임 입력 여부 검사
        if not nickname:
            return render(request, 'auth/nickname_setup.html', {'error': '닉네임을 입력해주세요'})
        # 닉네임 중복 여부 검사
        if Profile.objects.filter(nickname=nickname).exists(): 
            return render(request, "auth/nickname_setup.html", {'error': '이미 존재하는 닉네임입니다', 'nickname': nickname})
        # 닉네임 유효성 검사
        if len(nickname) > 10:
            return render(request, 'auth/nickname_setup.html', {'error': '최대 10자까지 입력 가능합니다', 'nickname': nickname})
        
        profile = Profile.objects.get(user=request.user)
        profile.nickname = nickname
        profile.save()
        return redirect('home_main')

    return render(request, 'auth/nickname_setup.html')

def mypage_main(request):
    # 로그인 여부 확인
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    context = {
        'user': request.user,
    }
    
    return render(request, 'mypage/mypage_main.html', context)

def delete_account(request):
    user = request.user
    user.delete() 
    logout(request) 
    return redirect('onboarding')
    
def change_password(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.method == 'POST':
        current_password = request.POST.get(
            'current_password', ''
        )
        new_password = request.POST.get(
            'new_password', ''
        )

        if not request.user.check_password(current_password):
            return render(
                request,
                'mypage/mypage_change_password.html',
                {
                    'current_error':
                    '현재 비밀번호가 일치하지 않습니다'
                }
            )

        if len(new_password) < 8:
            return render(
                request,
                'mypage/mypage_change_password.html',
                {
                    'new_error':
                    '비밀번호는 8자리 이상이어야 합니다'
                }
            )

        special_chars = (
            "!@#$%^&*()_+-=[]{};:'\",.<>/?\\|~"
        )

        has_special = False

        for char in new_password:
            if char in special_chars:
                has_special = True
                break

        if not has_special:
            return render(
                request,
                'mypage/mypage_change_password.html',
                {
                    'new_error':
                    '비밀번호에는 특수문자가 포함되어야 합니다'
                }
            )

        request.user.set_password(new_password)
        request.user.save()

        update_session_auth_hash(
            request,
            request.user
        )

        return render(
            request,
            'mypage/mypage_change_password.html',
            {
                'success':
                '비밀번호가 변경되었습니다'
            }
        )

    return render(
        request,
        'mypage/mypage_change_password.html'
    )

def change_nickname(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        new_nickname = request.POST.get(
            'new_nickname', ''
        ).strip()

        if not new_nickname:
            return render(
                request,
                'mypage/mypage_change_nickname.html',
                {
                    'current_nickname': profile.nickname,
                    'error': '닉네임을 입력해주세요'
                }
            )

        if len(new_nickname) > 10:
            return render(
                request,
                'mypage/mypage_change_nickname.html',
                {
                    'current_nickname': profile.nickname,
                    'error': '닉네임은 최대 10자까지 입력 가능합니다'
                }
            )

        duplicate_nickname = (
            Profile.objects
            .filter(nickname=new_nickname)
            .exclude(user=request.user)
            .exists()
        )

        if duplicate_nickname:
            return render(
                request,
                'mypage/mypage_change_nickname.html',
                {
                    'current_nickname': profile.nickname,
                    'error': '이미 사용 중인 닉네임입니다'
                }
            )

        profile.nickname = new_nickname
        profile.save()

        return render(
            request,
            'mypage/mypage_change_nickname.html',
            {
                'current_nickname': profile.nickname,
                'success': '닉네임이 변경되었습니다'
            }
        )

    return render(
        request,
        'mypage/mypage_change_nickname.html',
        {
            'current_nickname': profile.nickname
        }
    )