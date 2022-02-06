from django.contrib import admin
from .models import Category, Product, Topping

class ToppingAdmin(admin.ModelAdmin):
    list_display = (
        'display_name',
    )


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Topping, ToppingAdmin)
