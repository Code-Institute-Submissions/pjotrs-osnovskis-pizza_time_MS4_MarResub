from django.contrib import admin

from .models import CheckoutOrder, CheckoutLineItem

class CheckoutLineItemAdminInline(admin.TabularInline):
    model = CheckoutLineItem
    readonly_fields = ('lineitem_total',)


class CheckoutAdmin(admin.ModelAdmin):
    inlines = (CheckoutLineItemAdminInline,)

    readonly_fields = ('order_id', 'date', 'order_total',)

    fields = ('order_id', 'date', 'f_name', 'l_name',
              'email', 'phone_number', 'street_address1',
              'street_address2', 'postcode', 'city',
              'order_total',)

    list_display = ('order_id', 'date', 'f_name', 'l_name',
                    'order_total',)
    
    ordering = ('-date',)

admin.site.register(CheckoutOrder, CheckoutAdmin)