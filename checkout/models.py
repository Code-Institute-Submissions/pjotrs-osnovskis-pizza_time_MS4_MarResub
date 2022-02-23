import uuid
from django.db import models
from django.db.models import Sum
from products.models import Product


class CheckoutOrder(models.Model):
    """ Checkout oreder model for customer to enter their details for order to be delivered """
    # Found other way to use UUID here:
    # https://stackoverflow.com/questions/32528224/how-to-use-uuid
    order_id = models.UUIDField(default=uuid.uuid4, max_length=32, editable=False, unique=True)
    f_name = models.CharField(max_length=50, null=False, blank=False)
    l_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)

    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    city = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=False, blank=False)

    date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0.00)

    original_order = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')

    def update_total(self):
        """ Update grand total"""
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        self.save()

    def save(self, *args, **kwargs):
        """ Save method """
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.order_id)


class CheckoutLineItem(models.Model):
    """ Seapating all orders in the checkout to access them."""
    order = models.ForeignKey(CheckoutOrder, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    size = models.CharField(max_length=2, null=True, blank=True)
    qty = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """ Override the original save method, set item total and update order total"""
        if self.size == "s":
            price = self.product.price_s
        elif self.size == "m":
            price = self.product.price_m
        elif self.size == "l":
            price = self.product.price_l

        self.lineitem_total = price * self.qty
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.size} {self.product.display_name} on order {self.order.order_id}'
