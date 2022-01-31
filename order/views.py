from django.shortcuts import render

def order(request):
    """ A view for an order """
    return render(request, 'order/order.html')