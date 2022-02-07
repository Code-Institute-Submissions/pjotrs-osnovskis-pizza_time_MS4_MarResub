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

class Size(models.Model):
    name = models.CharField(max_length=1, null=True, blank=True)
    display_name = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.display_name


class Topping(models.Model):
    """
    Toppings model
    """
    name = models.CharField(max_length=32)
    display_name = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=4, decimal_places=2, default='0.99')

    def __str__(self):
        return self.display_name



class Product(models.Model):
    """
    Product model - to add Products to DB
    """
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    display_name = models.CharField(max_length=254, null=True)
    toppings = models.ManyToManyField(Topping, blank=True)
    size = models.ForeignKey(Size, null=True, blank=True, on_delete=models.CASCADE)
    price_s = models.DecimalField(max_digits=4, decimal_places=2)
    price_m = models.DecimalField(max_digits=4, decimal_places=2)
    price_l = models.DecimalField(max_digits=4, decimal_places=2)
    image_path = models.ImageField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.display_name