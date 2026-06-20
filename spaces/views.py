import uuid
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

def home_main(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    search = request.GET.get('search', '')

    spaces = Space.objects.filter(is_public=True).order_by('-created_at')

    if search:
        spaces = spaces.filter(
            Q(name__icontains=search) | Q(keyword__icontains=search)
        )
        
    active_spaces = []

    for space in spaces:
        end_date = space.created_at + timedelta(days=space.duration_days)
        current_members = space.members.count()

        if timezone.now() < end_date and current_members < space.max_capacity:
            active_spaces.append(space)

    # 테스트코드 ==============================
    print("\n" + "="*40)
    print(f"현재 로그인한 유저: {request.user}")
    print(f"현재 동작하는 우주 개수: {len(active_spaces)}개")
    for space in active_spaces:
        print(f"방 이름: {space.name}")
    print("="*40 + "\n")
    # 테스트코드 ==============================

    return render(request, 'home/home_main.html', {
        'spaces': active_spaces, 
        'search': search
    })

def space_create_step1(request):
    if request.method == 'POST':
        space_name = request.POST['space_name']
        space_keyword = request.POST.get('space_keyword', '')

        if len(space_name) == 0 or len(space_name) > 15 or len(space_keyword) > 15:
            return render(request, 'home/home_create_room1.html', {'error': '조건을 확인해주세요.'})
        
        if space_keyword == "":
            space_keyword = space_name

        return render(request, 'home/home_create_room2.html', {
            'space_name': space_name,
            'space_keyword': space_keyword
        })
    return render(request, 'home/home_create_room1.html')

def space_create_step2(request):
    if request.method == 'POST':
        space_name = request.POST['space_name']
        space_keyword = request.POST['space_keyword']
        operation_period = request.POST['operation_period']
        member_count = request.POST['member_count']

        is_public_checked = 'is_public' in request.POST
        
        if not operation_period.isdigit() or not member_count.isdigit():
            return render(request, 'home/home_create_room2.html', {
                'space_name': space_name,
                'space_keyword': space_keyword,
                'error': '조건을 확인해주세요.'
            })
        
        operation_period = int(operation_period)
        member_count = int(member_count)

        if member_count > 12 or member_count <= 0 or operation_period < 30 or operation_period > 365:
            return render(request, 'home/home_create_room2.html', {
                'space_name': space_name,
                'space_keyword': space_keyword,
                'error': '조건을 확인해주세요.'
            })

        return render(request, 'home/home_create_room3.html', {
            'space_name': space_name,
            'space_keyword': space_keyword,
            'operation_period': operation_period,
            'member_count': member_count,
            'is_public': is_public_checked
        })
    return redirect('spaces:home_create_room1')


def space_create_step3(request):
    if request.method == 'POST':
        space_name = request.POST['space_name']
        space_keyword = request.POST['space_keyword']
        operation_period = request.POST['operation_period']
        member_count = request.POST['member_count']
        is_public = request.POST['is_public']

        record_cycle = request.POST['record_cycle']
        record_limit = request.POST['record_limit']

        new_space = Space()
        new_space.name = space_name
        new_space.keyword = space_keyword
        new_space.duration_days = int(operation_period)
        new_space.max_capacity = int(member_count)
    
        if is_public == 'True':
            new_space.is_public = True
        else:
            new_space.is_public = False

        new_space.record_cycle = record_cycle
        new_space.record_limit = record_limit
        random_token = uuid.uuid4().hex[:6].upper()
        new_space.invite_token = random_token

        new_space.save()
        SpaceMember.objects.create(user=request.user, space=new_space)

        return redirect('spaces:home_main')
    return redirect('spaces:home_create_room1')

def join_space(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.method == 'POST':
        invite_code = request.POST.get('invite_code', '').strip().upper()
        target_space = Space.objects.filter(invite_token=invite_code).first()
        user = request.user

        if target_space:
            end_date = target_space.created_at + timedelta(days=target_space.duration_days)

            if timezone.now() >= end_date:
                return render(request, 'home/home_join_room.html', {
                    'error': '운영 기간이 종료된 우주입니다.'
                })

            if SpaceMember.objects.filter(user=user, space=target_space).exists():
                return redirect('spaces:space_main')

            current_members_count = SpaceMember.objects.filter(space=target_space).count()

            if current_members_count >= target_space.max_capacity:
                return render(request, 'home/home_join_room.html', {
                    'error': '이 우주는 이미 정원이 꽉 찼습니다.'
                })

            SpaceMember.objects.create(user=user, space=target_space)

            return redirect('spaces:space_main')
        else:
            return render(request, 'home/home_join_room.html', {
                'error': '코드나 링크가 올바르지 않습니다'
            })
        
    return render(request, 'home/home_join_room.html')

def home_room_detail(request, space_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    space = get_object_or_404(Space, space_id=space_id, is_public=True)

    end_date = space.created_at + timedelta(days=space.duration_days)

    if timezone.now() >= end_date:
        return redirect('spaces:home_main')

    d_day = (end_date.date() - timezone.now().date()).days

    current_members = space.members.count()

    return render(request, 'home/home_room_detail.html', {
        'space': space,
        'current_members': current_members,
        'd_day': d_day
    })

def space_main(request):
    my_spaces = Space.objects.filter(members__user=request.user)
    active_spaces = []

    for space in my_spaces:
        end_date = space.created_at + timedelta(days=space.duration_days)
        
        if timezone.now() < end_date:
            active_spaces.append(space)
    # 테스트코드 ==============================
    print("\n" + "="*40)
    print(f"현재 로그인한 유저: {request.user}")
    print(f"현재 동작하는 우주 개수: {len(active_spaces)}개")
    for space in active_spaces:
        print(f"방 이름: {space.name}")
    print("="*40 + "\n")
    # 테스트코드 ==============================

    return render(request, 'space/space_main.html', {'spaces': active_spaces})

def space_room(request, space_id):
    space = get_object_or_404(Space, pk=space_id)
    return render(request, 'space/space_room.html', {'space': space})

def home_room_detail(request, space_id):
    space = get_object_or_404(Space, pk=space_id)

    current_members = SpaceMember.objects.filter(space=space).count()

    return render(
        request,
        'home/home_room_detail.html',
        {
            'space': space,
            'current_members': current_members,
        }
    )