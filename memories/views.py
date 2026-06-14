from django.shortcuts import render, redirect
from spaces.models import Space

def memory_main(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    my_memories = Space.objects.filter(members__user=request.user)
    return render(request, 'memory/memory_main.html', {'memories': my_memories})
