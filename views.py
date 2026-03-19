@login_required
def cart(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    items = []
    total = 0

    for p in products:
        qty = cart[str(p.id)]
        p.qty = qty
        p.subtotal = p.price * qty
        total += p.subtotal
        items.append(p)

    return render(request, 'cart.html', {'products': items, 'total': total})
    @login_required
def checkout(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    total = sum(p.price * cart[str(p.id)] for p in products)

    if request.method == "POST":
        order = Order.objects.create(user=request.user, total=total)

        for p in products:
            OrderItem.objects.create(
                order=order,
                product=p,
                quantity=cart[str(p.id)]
            )

        request.session['cart'] = {}
        return redirect('payment', order.id)

    return render(request, 'checkout.html', {'total': total})
