from django.shortcuts import render
from .models import Category, Pizza, Drink

def products(request):
    """ A view to return a products page, including sorting and searching """

    all_pizzas = Pizza.objects.all()
    all_drinks = Drink.objects.all()
    categories = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category']
            pizzas = all_pizzas.filter(category__name=categories)
            drinks = all_drinks.filter(category__name=categories)
            categories = Category.objects.filter(name=categories)
        

    context = {
        'pizzas': pizzas,
        'drinks': drinks,
        'current_category': categories,
    }

    return render(request, 'products/products.html', context)