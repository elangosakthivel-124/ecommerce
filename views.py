from .models import Product, Order, OrderItem


@login_required
def cart(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0

    for pid, qty in cart.items():
        product = Product.objects.get(id=pid)
        product.qty = qty
        product.subtotal = qty * product.price
        total += product.subtotal
        products.append(product)

    return render(request, 'cart.html', {'products': products, 'total': total})


@login_required
def add_qty(request, id):
    cart = request.session.get('cart', {})
    cart[str(id)] += 1
    request.session['cart'] = cart
    return redirect('cart')


@login_required
def sub_qty(request, id):
    cart = request.session.get('cart', {})
    if cart[str(id)] > 1:
        cart[str(id)] -= 1
    request.session['cart'] = cart
    return redirect('cart')


@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    total = 0

    for pid, qty in cart.items():
        product = Product.objects.get(id=pid)
        total += qty * product.price

    if request.method == "POST":
        order = Order.objects.create(user=request.user, total=total)

        for pid, qty in cart.items():
            OrderItem.objects.create(
                order=order,
                product=Product.objects.get(id=pid),
                quantity=qty
            )

        request.session['cart'] = {}
        return redirect('home')

    return render(request, 'checkout.html', {'total': total})

@login_required
def dashboard(request):
    orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, 'dashboard.html', {'orders': orders})


@login_required
def order_detail(request, id):
    order = Order.objects.get(id=id, user=request.user)
    items = order.items.all()
    return render(request, 'order_detail.html', {'order': order, 'items': items})

@login_required
def payment(request, id):
    order = Order.objects.get(id=id, user=request.user)

    if request.method == "POST":
        # Dummy payment success
        order.status = 'paid'
        order.save()
        return redirect('success', id=order.id)

    return render(request, 'payment.html', {'order': order})


@login_required
def success(request, id):
    order = Order.objects.get(id=id, user=request.user)
    return render(request, 'success.html', {'order': order})
@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    total = 0

    for pid, qty in cart.items():
        product = Product.objects.get(id=pid)
        total += qty * product.price

    if request.method == "POST":
        order = Order.objects.create(user=request.user, total=total)

        for pid, qty in cart.items():
            OrderItem.objects.create(
                order=order,
                product=Product.objects.get(id=pid),
                quantity=qty
            )

        request.session['cart'] = {}
        return redirect('payment', id=order.id)

    return render(request, 'checkout.html', {'total': total})

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profile.phone = request.POST['phone']
        profile.address = request.POST['address']
        profile.save()

    return render(request, 'profile.html', {'profile': profile})


@login_required
def admin_orders(request):
    if not request.user.is_staff:
        return redirect('home')

    orders = Order.objects.all().order_by('-created')
    return render(request, 'admin_orders.html', {'orders': orders})

ShippingAddress.objects.create(
    order=order,
    full_name=request.user.username,
    phone=request.POST.get('phone', ''),
    address=request.POST.get('address', '')
)




