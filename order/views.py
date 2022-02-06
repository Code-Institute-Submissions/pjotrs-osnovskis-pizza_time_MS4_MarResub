from django.shortcuts import redirect, render

def order(request):
    """ A view for an order """
    return render(request, 'order/order.html')

def add_to_order(request, item_id):
    """ Add selected product to order"""

    size = float(request.POST.get('size'))
    redirect_url = request.POST.get('redirect_url')
    order = request.session.get('order', {})

    order[item_id] = size

    request.session['order'] = order
    print(request.session['order'])
    return redirect(redirect_url)