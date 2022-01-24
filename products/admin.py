from django.contrib import admin
from .models import Category, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price_s',
        'price_m',
        'price_l',
        'image',
    )

    ordering = ('name',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)