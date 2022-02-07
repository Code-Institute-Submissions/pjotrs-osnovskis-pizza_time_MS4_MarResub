from django.shortcuts import render
from .models import Category, Product

def products(request):
    """ A view to return a products page, including sorting and searching """

    all_products = Product.objects.all()
    categories = None
    products = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category']
            products = all_products.filter(category__name=categories)
            categories = Category.objects.filter(name=categories)

    context = {
        'products': products,
        'current_category': categories,
    }

    return render(request, 'products/products.html', context)