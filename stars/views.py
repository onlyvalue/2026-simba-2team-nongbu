from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from spaces.models import Space, SpaceMember
from django.utils import timezone

def create(request, space_id):
    if request.method == 'POST':
        space = get_object_or_404(Space, pk=space_id)

        is_member = SpaceMember.objects.filter(user=request.user, space=space).exists()
        if not is_member:
            return redirect('spaces:space_room', space_id=space_id)
        
        if space.record_limit == 'once':
            today = timezone.localdate()

            already_uploaded_today = Star.object.filter(
                space=space,
                user=request.user,
                created_at__date=today
            ).exists()

            if already_uploaded_today:
                return render(request, 'space/space_upload.html', {
                    'space':space,
                    'error': '오늘은 이미 기록을 남기셨네요 :)'
                })

        new_star = Star()
        new_star.image = request.FILES.get('image')
        new_star.content = request.POST.get('content', '')
        new_star.space = space
        new_star.user = request.user
        new_star.save()

        return redirect('spaces:space_room', space_id=space_id)
    
    return redirect('spaces:space_room', space_id=space_id)

def new_star(request, space_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    space = get_object_or_404(Space, pk=space_id)
    
    is_member = SpaceMember.objects.filter(user=request.user, space=space).exists()
    if not is_member:
        return redirect('spaces:space_room', space_id=space_id)
    
    return render(request, 'space/space_upload.html', {'space': space})

