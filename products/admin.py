from django.contrib import admin
from .models import Category, Product, Topping

class ToppingAdmin(admin.ModelAdmin):
    list_display = (
        'display_name',
    )
    exclude = (
        'name',
    )

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'display_name',
    )
    exclude = (
        'name',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Topping, ToppingAdmin)
