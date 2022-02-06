from django.shortcuts import get_object_or_404
from products.models import Product

def order_contents(request):

    order_items = []
    total = 0
    product_count = 0
    order = request.session.get('order', {})

    for item_id, qty in order.items():
        product = get_object_or_404(Product, pk=item_id)
        if product.price_s:
            total += qty * float(product.price_s)
        elif product.price_m:
            total += qty * float(product.price_m)
        elif product.price_l:
            total += qty * float(product.price_l)

        product_count += qty

        order_items.append({
            'item_id': item_id,
            'qty': qty,
            'product': product,
        })

    for item_id, price in order.items():
        product = get_object_or_404(Product, pk=item_id)
        if product.price_s:
            price = product.price_s
        elif product.price_m:
            price = product.price_m
        elif product.price_l:
            price = product.price_l

        order_items.append({
            'price': price,
        })


    grand_total = total # will keep this simple for now, will add delivery logic later

    context = {
        'order_items': order_items,
        'total': total,
        'product_count': product_count,
        'grand_total': grand_total,
    }

    return context