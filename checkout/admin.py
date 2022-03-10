from django.contrib import admin

from .models import CheckoutOrder, CheckoutLineItem


class CheckoutLineItemAdminInline(admin.TabularInline):
    model = CheckoutLineItem
    readonly_fields = ('lineitem_total',)


class CheckoutAdmin(admin.ModelAdmin):
    inlines = (CheckoutLineItemAdminInline,)

    readonly_fields = ('order_id', 'date', 'order_total',
                       'original_order', 'stripe_pid',)

    fields = ('order_id', 'user_profile', 'date', 'f_name',
              'email', 'phone_number', 'street_address1',
              'street_address2', 'postcode', 'city',
              'order_total', 'original_order', 'stripe_pid',)

    list_display = ('order_id', 'date', 'f_name',
                    'order_total',)

    ordering = ('-date',)

admin.site.register(CheckoutOrder, CheckoutAdmin)
