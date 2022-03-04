from django.shortcuts import render
from home.models import Address

def info(request):
    """ A view to return an info page """
    address = Address.objects.all()
    context = {
        'address': address
    }

    return render(request, 'business_info/base.html', context)
