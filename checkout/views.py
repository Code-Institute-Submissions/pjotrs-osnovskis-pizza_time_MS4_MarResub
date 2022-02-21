from django.shortcuts import redirect, render, reverse
from django.contrib import messages

from .forms import CheckoutForm

def checkout(request):
    order = request.session.get('order', {})

    if not order:
        messages.error(request, "There is nothing in your order just yet.")
        return redirect(reverse('products'))
    
    order_form = CheckoutForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
    }

    return render(request, template, context)