from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from spaces.models import Space, SpaceMember

def create(request, space_id):
    if request.method == 'POST':
        space = get_object_or_404(Space, pk=space_id)

        is_member = SpaceMember.objects.filter(user=request.user, space=space).exists()
        if not is_member:
            return redirect('spaces:space_room', space_id=space_id)

        new_star = Star()
        new_star.image = request.FILES.get('image')
        new_star.content = request.POST.get('content', '')
        new_star.space = space
        new_star.user = request.user
        new_star.save()

        return redirect('spaces:space_room', space_id=space_id)
    
    return redirect('spaces:space_room', space_id=space_id)

def new_star(request, space_id):
    space = get_object_or_404(Space, pk=space_id)
    
    is_member = SpaceMember.objects.filter(user=request.user, space=space).exists()
    if not is_member:
        return redirect('spaces:space_room', space_id=space_id)
    
    return render(request, 'space/space_upload.html', {'space': space})

