from tkinter import CASCADE
from django.db import models

class Category(models.Model):
    """ 
    Category model, includes name and full name in case needed
    Returns both, name and full name.
    """

    class Meta:
        """ Spelling correction for admin page"""
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    full_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_full_name(self):
        return self.full_name


class Topping(models.Model):
    """
    Toppings model
    """
    name = models.CharField(max_length=32)
    display_name = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=4, decimal_places=2, default='0.99')


class Pizza(models.Model):
    """
    Pizza model - to add Pizzas to DB
    """
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    display_name = models.CharField(max_length=254, null=True)
    toppings = models.ManyToManyField(Topping)
    price_s = models.DecimalField(max_digits=4, decimal_places=2)
    price_m = models.DecimalField(max_digits=4, decimal_places=2)
    price_l = models.DecimalField(max_digits=4, decimal_places=2)
    image_path = models.ImageField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.display_name




class Product(models.Model):
    """
    Products model. Will be used to POST as a new order item
    """
    total_price = models.DecimalField(max_digits=4, decimal_places=2)
    rating = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)

    def __str__(self):
        return self.pizza.name


    def __str__(self):
        return self.display_name


class Drink(models.Model):
    """
    Drink model
    """
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    display_name = models.CharField(max_length=254, null=True)
    price_s = models.DecimalField(max_digits=4, decimal_places=2)
    price_m = models.DecimalField(max_digits=4, decimal_places=2)
    price_l = models.DecimalField(max_digits=4, decimal_places=2)
    image_path = models.ImageField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.display_name
