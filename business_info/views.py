from django.shortcuts import render

import os
if os.path.exists("env.py"):
    import env


def info(request):
    """ A view to return an info page """
    return render(request, 'business_info/about.html')


def contact_us(request):
    """ A view to return an info page """
    email_js_access_token = os.environ.get('EMAILJS_API_KEY')
    context = {
        'email_js_access_token': email_js_access_token,
    }
    return render(request, 'business_info/contact.html', context)
