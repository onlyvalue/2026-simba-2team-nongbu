import uuid
from django.shortcuts import render, redirect, get_object_or_404
from .models import *

# Create your views here.
def home_main(request):
    spaces = Space.objects.all().order_by('-created_at')
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
    return redirect('home_create_room1')


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

def home_join_room(request):
    if request.method == 'POST':
        invite_code = request.POST['invite_code']
        target_space = Space.objects.filter(invite_token=invite_code).first()

        if target_space:
            return redirect('home_main')
        else:
            return render(request, 'home/home_join_room.html', {'error': '올바른 코드가 아닙니다. 다시 확인해주세요.'})
        
    return render(request, 'home/home_join_room.html')