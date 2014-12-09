from django.shortcuts import render

# Create your views here.

def submit(request):
    return render(request, 'users/submit.html', {})

def profile(request):
    return render(request, 'users/profile.html', {})
