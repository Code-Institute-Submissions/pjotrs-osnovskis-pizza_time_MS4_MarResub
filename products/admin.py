from django.contrib import admin
from .models import Category, Product, Pizza, Topping, Drink

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Drink)
admin.site.register(Pizza)
admin.site.register(Topping)
