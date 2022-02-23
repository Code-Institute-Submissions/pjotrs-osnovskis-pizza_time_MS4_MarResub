from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm
from checkout.models import CheckoutOrder

def user_profile(request):
    """ Display users profile. """
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.POST:
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid:
            form.save()
            messages.success(request, 'Your profile has been updated successfully')

    form = UserProfileForm(instance=profile)
    orders = profile.orders.all()
    
    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True
    }

    return render(request, template, context)

def order_history(request, order_number):
    order = get_object_or_404(CheckoutOrder, order_id=order_number)

    messages.info(request, (
        f'This is a past order confirmation for order number: {order_number}'
        'A Confirmation email was sent on the order date'
    ))

    template = 'checkout/checkout_success.html'

    context = {
        'order': order,
    }

    return render(request, template, context)