from django.shortcuts import get_object_or_404
from products.models import Product, Size

def order_contents(request):

    order_items = []
    total = 0
    grand_total = 0
    item_count = 0
    order = request.session.get('order', {})
    qty = 0
    price = 0.00



    for item_id, item_data in order.items():
        if isinstance(item_data, int):
            product = get_object_or_404(Product, pk=item_id)
            total += item_data * price
            item_count += item_data
            order_items.append({
                'item_id': item_id,
                'qty': item_data,
                'product': product,
            })
        else:
            product = get_object_or_404(Product, pk=item_id)
            for size, qty in item_data['items_by_size'].items():
                if size == "s":
                    price = product.price_s
                elif size == "m":
                    price = product.price_m
                elif size == "l":
                    price = product.price_l

                total = qty * price
                grand_total += qty * price
                item_count += qty
                order_items.append({
                    'item_id': item_id,
                    'qty': qty,
                    'size': size,
                    'price': price,
                    'total': total,
                    'product': product,
                })

    context = {
        'order_items': order_items,
        'grand_total': grand_total,
        'item_count': item_count,
    }
    return context