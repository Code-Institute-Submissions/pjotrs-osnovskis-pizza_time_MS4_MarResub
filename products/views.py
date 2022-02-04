from django.shortcuts import render
from .models import Product, Category, Pizza, Topping

def products(request):
    """ A view to return a products page, including sorting and searching """

    products = Product.objects.all()
    pizzas = Pizza.objects.all()
    categories = None

    if request.GET:
            if 'category' in request.GET:
                categories = request.GET['category'].split(',')
                products = products.filter(category__name__in=categories)
                categories = Category.objects.filter(name__in=categories)

    context = {
        'products': products,
        'pizzas': pizzas,
        'current_category': categories,
    }

    return render(request, 'products/products.html', context)