from django.shortcuts import redirect, render

def order(request):
    """ A view for an order """
    return render(request, 'order/order.html')

def add_to_order(request, item_id):
    """ Add selected product to order"""

    qty = int(request.POST.get('qty'))
    price = float(request.POST.get('price'))
    redirect_url = request.POST.get('redirect_url')
    size = None

    if 'size' in request.POST:
        size = request.POST['size']
        print(size)
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

    # print(price)
    print(f"POST: {request.POST}")
    request.session['order'] = order
    return redirect(redirect_url)