from django.shortcuts import render
from home.models import Address

import os
if os.path.exists("env.py"):
    import env


def info(request):
    """ A view to return an info page """
    address = Address.objects.all()
    context = {
        'address': address
    }

    return render(request, 'business_info/about.html', context)

def contact_us(request):
    """ A view to return an info page """
    address = Address.objects.all()
    email_js_access_token = os.environ.get('EMAILJS_API_KEY')
    context = {
        'email_js_access_token': email_js_access_token,
        'address': address,
    }


    return render(request, 'business_info/contact.html', context)
