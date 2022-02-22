from locale import currency
from django.shortcuts import redirect, render, reverse
from django.contrib import messages
from django.conf import settings

from .forms import CheckoutForm
from order.contexts import order_contents

import stripe

import os
if os.path.exists("env.py"):
    import env


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY


    order = request.session.get('order', {})

    if not order:
        messages.error(request, "There is nothing in your order just yet.")
        return redirect(reverse('products'))
    
    current_order = order_contents(request)
    total = current_order['grand_total']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount = stripe_total,
        currency = settings.STRIPE_CURRENCY,
    )

    order_form = CheckoutForm()

    if not stripe_public_key:
        messages.error(request, ("Public key not found. \
            Did you set it up in environment?"))

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)