from django.shortcuts import get_object_or_404, redirect, render
from django.shortcuts import reverse, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import CheckoutForm
from order.contexts import order_contents

from .models import CheckoutOrder, CheckoutLineItem
from products.models import Product
from profiles.models import UserProfile
from profiles.forms import UserProfileForm

import stripe
import json

import os
if os.path.exists("env.py"):
    import env


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'order': json.dumps(request.session.get('order', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Your payment cannot be processed right now. \
            Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        checkout_order = request.session.get('order', {})
        form_data = {
            'f_name': request.POST['f_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'city': request.POST['city'],
            'postcode': request.POST['postcode'],
        }
        order_form = CheckoutForm(form_data)

        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_order = json.dumps(checkout_order)
            order.save()

            for item_id, item_data in checkout_order.items():
                try:
                    product = Product.objects.get(id=item_id)
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
                                qty=qty,
                                size=size,
                                product=product,
                            )
                            checkout_line_item.save()

                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your order wasn't\
                         found in our database."
                        "Please contact us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('order'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_id]))
        else:
            messages.error(request, 'There was an error, please\
                                     check your details and try again.')

    else:
        checkout_order = request.session.get('order', {})

        if not checkout_order:
            messages.error(request, "There is nothing in your\
                                     order just yet.")
            return redirect(reverse('products'))

        current_order = order_contents(request)
        total = current_order['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        # Try to automatically fill in the checkout form with
        # any info the user has in their profile
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = CheckoutForm(initial={
                    'f_name': profile.default_f_name,
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'postcode': profile.default_postcode,
                    'city': profile.default_city,
                })
            except UserProfile.DoesNotExist:
                order_form = CheckoutForm()
        else:
            order_form = CheckoutForm()

    if not stripe_public_key:
        messages.warning(request, ("Public key not found. \
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

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

        # Save the user's info
        if save_info:
            profile_data = {
                'default_f_name': order.f_name,
                'default_phone_number': order.phone_number,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_postcode': order.postcode,
                'default_city': order.city,
            }
            user_profile_form = UserProfileForm(profile_data,
                                                instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(request, f'Order {order_number} has been successfully\
                                processed. \n'
                     f'Confirmation has been sent to {order.email}')

    if 'order' in request.session:
        del request.session['order']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
