from django.shortcuts import redirect, render, reverse
from django.contrib import messages

from .forms import CheckoutForm

import os
if os.path.exists("env.py"):
    import env

os.environ.get("SECRET_KEY")

def checkout(request):
    order = request.session.get('order', {})

    if not order:
        messages.error(request, "There is nothing in your order just yet.")
        return redirect(reverse('products'))
    
    order_form = CheckoutForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': os.environ.get('STRIPE_PUB_KEY'),
        'client_secret': 'test_client_secret',
        # 'client_secret': os.environ.get('STRIPE_SECTET_KEY'),
    }

    return render(request, template, context)