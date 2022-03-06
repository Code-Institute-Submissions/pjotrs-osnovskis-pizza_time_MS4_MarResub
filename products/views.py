from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Category, Product
from home.models import Address
from .forms import ProductForm

def products(request):
    """ A view to return a products page, including sorting and searching """
    address = Address.objects.all()
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
        'address': address,
    }

    return render(request, 'products/products.html', context)


@login_required
def add_product(request):
    """ Add a product to the list """
    address = Address.objects.all()

    if not request.user.is_superuser:
        messages.error(request, 'Access denied.')
        return(reverse('home'))

    else:
        products = Product.objects.all()

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
            'products': products,
            'form': form,
            'address': address,

        }

        return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the list """
    address = Address.objects.all()
    if not request.user.is_superuser:
        messages.error(request, 'Access denied.')
        return redirect(reverse('home'))

    else:
        products = Product.objects.all()
        product = get_object_or_404(Product, pk=product_id)

        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                messages.success(request, 'Product successfully updated!')
                return redirect(request.META['HTTP_REFERER'])
            else:
                messages.error(request, 'Failed to update product. Please check the form and try again.')
        else:
            form = ProductForm(instance=product)
            messages.info(request, f'You are editing {product.display_name}')

        template = 'products/change_product.html'
        context = {
            'form': form,
            'product': product,
            'products': products,
            'address': address,

        }

        return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product """
    if not request.user.is_superuser:
        messages.error(request, 'Access denied.')
        return redirect(reverse('home'))

    else:
        product = get_object_or_404(Product, pk=product_id)
        product.delete()
        messages.success(request, f'Product {product.display_name} deleted!')
        return redirect(request.META['HTTP_REFERER'])


@login_required
def like_view(request, pk):
    product = get_object_or_404(Product, id=request.POST.get('liked_product_id'))
    product.likes.add(request.user)
    return redirect(request.META['HTTP_REFERER'])

@login_required
def remove_like(request, pk):
    product = get_object_or_404(Product, id=request.POST.get('liked_product_id'))
    product.likes.remove(request.user)
    return redirect(request.META['HTTP_REFERER'])

