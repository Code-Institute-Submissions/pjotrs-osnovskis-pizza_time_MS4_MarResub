from django.shortcuts import get_object_or_404, redirect, render, reverse, HttpResponse
from django.contrib import messages

from products.models import Product


def order(request):
    """ A view for an order """
    return render(request, 'order/order.html')


def add_to_order(request, item_id):
    """ Add selected product to order"""
    product = get_object_or_404(Product, pk=item_id)
    qty = int(request.POST.get('qty'))
    size = request.POST['size']

    # Give plural ending in needed.
    if qty == 1:
        ending = ""
    else:
        ending = "'s"

    # Give sizes an appropriate names
    if size == "s":
        size_name = "Small"
    elif size == "m":
        size_name = "Medium"
    else:
        size_name = "Large"

    order = request.session.get('order', {})

    if item_id in list(order.keys()):
        if size in order[item_id]['items_by_size'].keys():
            order[item_id]['items_by_size'][size] += qty
            messages.success(request, f'Perfect! {qty} more {size_name} {product.display_name}{ending} added to your order.')
        else:
            order[item_id]['items_by_size'][size] = qty
            messages.success(request, f'Amazing! {qty} {size_name} {product.display_name}{ending} added to your order.')
    else:
        order[item_id] = {'items_by_size': {size: qty}}
        messages.success(request, f'Great! {qty} {size_name} {product.display_name}{ending} added to your order.')

    request.session['order'] = order
    # After submitting "Add to order", stays on the same page. Idea taken from here:
    # https://stackoverflow.com/questions/39560175/redirect-to-same-page-after-post-method-using-class-based-views
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def change_order(request, item_id):
    """ Change selected product in the order"""
    product = get_object_or_404(Product, pk=item_id)
    qty = int(request.POST.get('qty'))
    size = request.POST['size']

    # Give plural ending in needed.
    if qty == 1:
        ending = ""
    else:
        ending = "'s"

    # Give sizes an appropriate names
    if size == "s":
        size_name = "Small"
    elif size == "m":
        size_name = "Medium"
    else:
        size_name = "Large"

    order = request.session.get('order', {})

    if qty > 0:
        order[item_id]['items_by_size'][size] = qty
        messages.success(request, f'Updated! There is {qty} {size_name} {product.display_name}{ending} in your order now.')
    else:
        del order[item_id]['items_by_size'][size]
        if not order[item_id]['items_by_size']:
            order.pop(item_id)

    request.session['order'] = order
    return redirect(reverse('order'))

def remove_from_order(request, item_id):
    """Remove the item from the shopping order"""
    product = get_object_or_404(Product, pk=item_id)

    try:
        size = request.POST['product_size']
        qty = request.POST['product_qty']

        # Give plural ending in needed.
        if qty == 1:
            ending = ""
        else:
            ending = "'s"

        # Give sizes an appropriate names
        if size == "s":
            size_name = "Small"
        elif size == "m":
            size_name = "Medium"
        else:
            size_name = "Large"

        order = request.session.get('order', {})

        del order[item_id]['items_by_size'][size]
        if not order[item_id]['items_by_size']:
            order.pop(item_id)
            messages.warning(request, f'You have removed {qty} {size_name} {product.display_name}{ending} from your order.')

        request.session['order'] = order
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item {e}.')
        return HttpResponse(status=500)