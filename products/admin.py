from django.contrib import admin
from .models import Category, Product, Pizza, Topping, Drink


# class ProductAdmin(admin.ModelAdmin):
#     """
#     Admin customization for Products section to show relevan information
#     for users convenience.
#     """
#     list_display = (
#     )

#     ordering = ('pizza',)

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Drink)
admin.site.register(Pizza)
admin.site.register(Topping)
