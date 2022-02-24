from django.shortcuts import render
from .models import Category, Product
from .forms import ProductForm


def products(request):
    """ A view to return a products page, including sorting and searching """

    all_products = Product.objects.all()
    categories = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category']
            all_products = all_products.filter(category__name=categories)
            categories = Category.objects.filter(name=categories)

    context = {
        'products': all_products,
        'current_category': categories,
    }

    return render(request, 'products/products.html', context)


def add_product(request):
    """ Add a product to the store """
    form = ProductForm()
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)