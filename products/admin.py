from django.contrib import admin
from .models import Category, Product


class ProductAdmin(admin.ModelAdmin):
    """
    Admin customization for Products section to show relevan information
    for users convenience.
    """
    list_display = (
        'name',
        'full_name',
        'category',
        'price_s',
        'price_m',
        'price_l',
        'image',
    )

    ordering = ('name',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)