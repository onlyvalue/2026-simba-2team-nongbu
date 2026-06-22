from django.shortcuts import render, redirect, get_object_or_404
from spaces.models import Space
from django.utils import timezone
from datetime import timedelta
import calendar
from spaces.constellation import CONSTELLATION_ORDER, CONSTELLATIONS

def memory_main(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    my_spaces = Space.objects.filter(members__user=request.user).order_by('-created_at')
    
    memories = []

    for space in my_spaces:
        end_date = space.created_at + timedelta(days=space.duration_days)
        if timezone.now() >= end_date:
            memories.append(space)

    # 테스트코드 ==============================
    print("\n" + "="*40)
    print(f"현재 로그인한 유저: {request.user}")
    print(f"추억에 담긴 우주 개수: {len(memories)}개")
    
    for memory in memories:
        print(f"방 이름: {memory.name}")
    print("="*40 + "\n")
    # 테스트코드 ==============================

    return render(request, 'memory/memory_main.html', {'memories': memories})

def memory_gallery_list(request, space_id):
    space = get_object_or_404(Space, pk=space_id)
    today = timezone.now()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    cal = calendar.Calendar(calendar.SUNDAY)

    prev_month = month - 1
    prev_year = year
    if prev_month == 0:
        prev_month = 12
        prev_year -= 1

    next_month = month + 1
    next_year = year
    if next_month == 13:
        next_month = 1
        next_year += 1

    month_name = calendar.month_name[month].upper()
    days_list = []
    for week in cal.monthdatescalendar(year, month):  
        for day in week:                              
            days_list.append(day) 

    context = {
        'space_id': space_id,
        'space' : space,
        'current_year': year,
        'current_month': month,
        'month_name': month_name,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'days_list': days_list,
    }
    return render(request, 'memory/memory_gallery_list.html', context)
                       


def memory_gallery(request):
    return render(request, 'memory/memory_gallery.html')


def memory_constellation(request, space_id):
    # 1. 로그인 체크
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    # 2. 유저가 소속된 방인지 확인하며 가져오기 (보안)
    space = get_object_or_404(
        Space.objects.filter(
            members__user=request.user).distinct(),
        space_id=space_id
    )

    # 3. 만료일자 계산
    end_datetime = space.created_at + timedelta(
        days=space.duration_days
    )

    # 4. 아직 만료되지 않았다면 튕겨내기
    if timezone.now() < end_datetime:
        return redirect('memories:memory_main')

    # 5. 저장된 별들 가져오기
    stars = space.stars.order_by('created_at')

    # ==========================================
    # 🌟 추가된 부분: 자바스크립트를 위한 별자리 계산 로직
    # ==========================================
    total_memory_count = stars.count()
    remain = total_memory_count
    render_constellations = []

    for name in CONSTELLATION_ORDER:
        constellation = CONSTELLATIONS[name]
        required = constellation["required"]

        current = min(remain, required)

        render_constellations.append({
            "name": name,
            "current": current,
            "required": required,
            "data": constellation,
        })

        remain -= required

        if remain <= 0:
            break
    # ==========================================

    # 6. HTML로 필요한 데이터 모두 넘기기
    return render(request, 'memory/memory_constellation.html', {
        'space': space,
        'stars': stars,
        'start_date': space.created_at.date(),
        'end_date': end_datetime.date(),
        'render_constellations': render_constellations, 
    })