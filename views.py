from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator
from django.db.models import Q
from .models import *

def register_user(request):
    if request.method=="POST":
        User.objects.create_user(
            username=request.POST['username'],
            email=request.POST['email'],
            password=request.POST['password']
        )
        return redirect('login')
    return render(request,'register.html')

def login_user(request):
    if request.method=="POST":
        user=authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user:
            login(request,user)
            return redirect('home')
    return render(request,'login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    q=request.GET.get('q')
    products=Product.objects.all()
    if q:
        products=products.filter(Q(name__icontains=q))
    paginator=Paginator(products,8)
    products=paginator.get_page(request.GET.get('page'))
    return render(request,'home.html',{'products':products})

@login_required
def add_to_cart(request,id):
    cart=request.session.get('cart',{})
    cart[str(id)]=cart.get(str(id),0)+1
    request.session['cart']=cart
    return redirect('cart')

@login_required
def cart(request):
    cart=request.session.get('cart',{})
    items=[]
    total=0
    for pid,qty in cart.items():
        p=Product.objects.get(id=pid)
        p.qty=qty
        p.subtotal=p.price*qty
        total+=p.subtotal
        items.append(p)
    return render(request,'cart.html',{'products':items,'total':total})

@login_required
def checkout(request):
    cart=request.session.get('cart',{})
    total=sum(Product.objects.get(id=i).price*q for i,q in cart.items())
    if request.method=="POST":
        order=Order.objects.create(user=request.user,total=total)
        for pid,qty in cart.items():
            OrderItem.objects.create(order=order,product_id=pid,quantity=qty)
        request.session['cart']={}
        return redirect('payment',order.id)
    return render(request,'checkout.html',{'total':total})

@login_required
def payment(request,id):
    order=Order.objects.get(id=id)
    if request.method=="POST":
        order.status='paid'
        order.save()
        return redirect('success',id)
    return render(request,'payment.html',{'order':order})

@login_required
def success(request,id):
    return render(request,'success.html')

@login_required
def dashboard(request):
    orders=Order.objects.filter(user=request.user)
    return render(request,'dashboard.html',{'orders':orders})
