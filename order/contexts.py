
def order_contents(request):

    order_items = []
    total = 0
    product_count = 0

    grand_total = total # will keep this simple for now, will add delivery logic later

    context = {
        'order_items': order_items,
        'total': total,
        'product_count': product_count,
        'grand_total': grand_total,
    }

    return context