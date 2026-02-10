from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Product


@login_required
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


@login_required
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})


@login_required
def add_to_cart(request, id):
    cart = request.session.get('cart', {})
    cart[str(id)] = cart.get(str(id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')


@login_required
def cart(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0

    for pid, qty in cart.items():
        product = Product.objects.get(id=pid)
        product.qty = qty
        product.subtotal = qty * float(product.price)
        total += product.subtotal
        products.append(product)

    return render(request, 'cart.html', {'products': products, 'total': total})


@login_required
def remove_cart(request, id):
    cart = request.session.get('cart', {})
    if str(id) in cart:
        del cart[str(id)]
    request.session['cart'] = cart
    return redirect('cart')


# AUTH (Day 2)

def register_user(request):
    if request.method == "POST":
        User.objects.create_user(
            username=request.POST['username'],
            email=request.POST['email'],
            password=request.POST['password']
        )
        return redirect('login')
    return render(request, 'register.html')


def login_user(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('login')
