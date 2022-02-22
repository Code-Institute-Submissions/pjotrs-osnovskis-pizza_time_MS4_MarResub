from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib import messages
from django.conf import settings

from .forms import CheckoutForm
from order.contexts import order_contents

from .models import CheckoutOrder, CheckoutLineItem
from products.models import Product

import stripe

import os
if os.path.exists("env.py"):
    import env


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    
    if request.method == 'POST':
        checkout_order = request.session.get('order', {})
        form_data = {
            'f_name': request.POST['f_name'],
            'l_name': request.POST['l_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'city': request.POST['city'],
            'postcode': request.POST['postcode'],
        }

        order_form = CheckoutForm(form_data)
        if order_form.is_valid():
            order = order_form.save()
            
            for item_id, item_data in checkout_order.items():
                try:
                    product = Product.objects.get(pk=item_id)
                    if isinstance(item_data, int):
                        checkout_line_item = CheckoutLineItem(
                            order=order,
                            product=product,
                            qty=item_data,
                        )
                        checkout_line_item.save()
                    else:
                        for size, qty in item_data['items_by_size'].items():
                            checkout_line_item = CheckoutLineItem(
                                order=order,
                                qty = qty,
                                size = size,
                                product = product,
                            )
                            checkout_line_item.save()

                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your order wasn't found in our database."
                        "Please contact us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('order'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_id]))
        else:
            messages.error(request, 'There was an error, please check your details and try again.')

    else:
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


def checkout_success(request, order_number):
    """ Successful Checkout View"""
    save_info = request.session.get('save_info')
    order = get_object_or_404(CheckoutOrder, order_id=order_number)
    messages.success(request, f'Order {order_number} has been successfully processed. \n'
        f'Confirmation has been sent to {order.email}')
    
    if 'order' in request.session:
        del request.session['order']
    
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)