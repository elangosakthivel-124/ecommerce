from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Product

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def register_user(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created")
        return redirect('login')

    return render(request, 'register.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('login')

from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

