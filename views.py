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
