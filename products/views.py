from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages

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

    """ Add a product to the list """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product was added successfully')
            return redirect(reverse('add_product'))
        else:
            messages.error(request, 'Failed to add product. Please check the form and try again.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)