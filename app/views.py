from django.shortcuts import render

def mainpage(request):
    return render(request, 'mainpage.html')
# Create your views here.
def onboarding(request):
    return render(request, 'onboarding.html')