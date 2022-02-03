from sre_parse import CATEGORIES
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


class Product(models.Model):
    """
    Products model, is assigned to category model via ForeignKey.
    Includes: name, ingredients, price for small, medium and large sizes, rating, image
    Returns name.
    """
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    full_name = models.CharField(max_length=254, null=True)
    ingredients = models.ForeignKey('Pizza', null=True, blank=True, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    size = models.CharField(max_length=8)
    rating = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

class Topping(models.Model):
    """
    Toppings model
    """
    name = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.name


class Pizza(models.Model):
    """
    Pizza model
    """
    PIZZA_SIZES = (
        ('S', '22 CM'),
        ('M', '32 CM'),
        ('L', '40 CM'),
    )

    name = models.CharField(max_length=254)
    full_name = models.CharField(max_length=254, null=True)
    toppings = models.ManyToManyField(Topping)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    size = models.CharField(max_length=1, choices=PIZZA_SIZES)
    date_added = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.full_name
