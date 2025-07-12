from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .forms import RegisterForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('landing')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_instructor:
                return redirect('instructor:instructor_dashboard')
            else:
                return redirect('landing')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')
