from django.shortcuts import redirect, render, reverse, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages

from products.models import Product

def order(request):
    """ A view for an order """
    return render(request, 'order/order.html')

def add_to_order(request, item_id):
    """ Add selected product to order"""
    product = Product.objects.get(pk=item_id)
    qty = int(request.POST.get('qty'))
    size = None

    if 'size' in request.POST:
        size = request.POST['size']
        ending = ""
        if qty == 1:
            ending = ""
        else:
            ending = "'s"

    order = request.session.get('order', {})
    
    if size:
        if item_id in list(order.keys()):
            if size in order[item_id]['items_by_size'].keys():
                order[item_id]['items_by_size'][size] += qty
                messages.success(request, f'Done! {qty} more {size} {product.display_name}{ending} added to your order.')
            else:
                order[item_id]['items_by_size'][size] = qty
                messages.success(request, f'Done! {qty} {size} {product.display_name}{ending} added to your order.')
        else:
            order[item_id] = {'items_by_size': {size: qty}}
            messages.success(request, f'Done! {qty} {size} {product.display_name}{ending} added to your order.')
    else:
        if item_id in list(order.keys()):
            order[item_id] += qty
        else:
            order[item_id] = qty    
            

    request.session['order'] = order
    # After submitting "Add to order", stays on the same page. Idea taken from here:
    # https://stackoverflow.com/questions/39560175/redirect-to-same-page-after-post-method-using-class-based-views
    return redirect("/products/?category=pizza")

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
    product = Product.objects.get(pk=item_id)

    try:
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        order = request.session.get('order', {})

        if size:
            del order[item_id]['items_by_size'][size]
            if not order[item_id]['items_by_size']:
                order.pop(item_id)
                messages.warning(request, f'Done! {product.display_name} removed.')
                
        else:
            order.pop(item_id)
            
        request.session['order'] = order
        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(status=500)