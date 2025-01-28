from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from main.models import CharBase


@login_required
def profile(request):
    print("Current account: ", request.user)
    characters = CharBase.objects.filter(owner=request.user)
    return render(request, 'main/profile.html', {'characters': characters})

