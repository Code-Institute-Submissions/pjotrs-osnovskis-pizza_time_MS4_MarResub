from django.shortcuts import redirect, render

def order(request):
    """ A view for an order """
    return render(request, 'order/order.html')

def add_to_order(request, item_id):
    """ Add selected product to order"""

    quantity = int(request.POST.get('qty'))
    price = float(request.POST.get('size'))
    redirect_url = request.POST.get('redirect_url')
    order = request.session.get('order', {})

    if item_id in list(order.keys()):
        order[item_id] += quantity
    else:
        order[item_id] = quantity

    request.session['order'] = order
    return redirect(redirect_url)