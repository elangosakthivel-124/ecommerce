from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product, Category


@login_required
def home(request):
    query = request.GET.get('q')
    cat_id = request.GET.get('category')

    products = Product.objects.all()
    categories = Category.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    if cat_id:
        products = products.filter(category_id=cat_id)

    paginator = Paginator(products, 8)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    return render(request, 'home.html', {
        'products': products,
        'categories': categories
    })
