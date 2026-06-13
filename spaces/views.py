import uuid
from django.shortcuts import render, redirect, get_object_or_404
from .models import *

def home_main(request):
    spaces = Space.objects.filter(is_public=True).order_by('-created_at') # 공개 된 우주만 최신 순으로 가져오기
    return render(request, 'home/home_main.html', {'spaces':spaces})

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

        return redirect('home_main')
    return redirect('home_create_room1')

def join_space(request):
    if request.method == 'POST':
        invite_code = request.POST.get('invite_code')
        target_space = Space.objects.filter(invite_token=invite_code).first()
        user = request.user

        if target_space:
            current_members_count = SpaceMember.objects.filter(space=target_space).count()

            if not SpaceMember.objects.filter(user=user, space=target_space).exists():
                SpaceMember.objects.create(user=user, space=target_space)
            
            if current_members_count >= target_space.max_capacity:
                return render(request, 'home/home_join_room.html', {'error': '이 우주는 이미 정원이 꽉 찼습니다.'})

            return redirect('spaces:space_main')
        else:
            return render(request, 'home/home_join_room.html', {'error': '올바른 코드가 아닙니다. 다시 확인해주세요.'})
        
    return render(request, 'home/home_join_room.html')

def space_main(request):
    my_spaces = Space.objects.filter(members__user=request.user)
    return render(request, 'space/space_main.html', {'spaces': my_spaces})

def space_room(request, space_id):
    space = get_object_or_404(Space, pk=space_id)
    return render(request, 'space/space_room.html', {'space': space})
