from django.shortcuts import render
from .models import Address

def index(request):
    """ A view to return an index page """
    address = Address.objects.all()
    context = {
        'address': address
    }

    return render(request, 'home/pages/index.html', context)

