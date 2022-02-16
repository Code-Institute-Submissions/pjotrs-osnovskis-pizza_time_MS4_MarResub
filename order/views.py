from django.shortcuts import redirect, render, reverse, HttpResponse

def order(request):
    """ A view for an order """
    return render(request, 'order/order.html')

def add_to_order(request, item_id):
    """ Add selected product to order"""

    qty = int(request.POST.get('qty'))
    redirect_url = request.POST.get('redirect_url')
    size = None

    if 'size' in request.POST:
        size = request.POST['size']

    order = request.session.get('order', {})

    if size:
        if item_id in list(order.keys()):
            if size in order[item_id]['items_by_size'].keys():
                order[item_id]['items_by_size'][size] += qty
            else:
                order[item_id]['items_by_size'][size] = qty
        else:
            order[item_id] = {'items_by_size': {size: qty}}
    else:
        if item_id in list(order.keys()):
            order[item_id] += qty
        else:
            order[item_id] = qty    
    
    request.session['order'] = order
    return redirect(redirect_url)


def change_order(request, item_id):
    """ Change selected product in the order"""
    qty = int(request.POST.get('qty'))
    size = None

    if 'size' in request.POST:
        size = request.POST.get('size')

    order = request.session.get('order', {})

  
    if size:
        if qty > 0:
            order[item_id]['items_by_size'][size] = qty
        else:
            del order[item_id]['items_by_size'][size]
            if not order[item_id]['items_by_size']:
                order.pop(item_id)
    else:
        if qty > 0:
            order[item_id] = qty
        else:
            order.pop(item_id)


    request.session['order'] = order
    return redirect(reverse('order'))

def remove_from_order(request, item_id):
    """Remove the item from the shopping order"""

    try:
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        order = request.session.get('order', {})

        if size:
            del order[item_id]['items_by_size'][size]
            if not order[item_id]['items_by_size']:
                order.pop(item_id)
        else:
            order.pop(item_id)

        request.session['order'] = order
        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(status=500)