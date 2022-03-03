from django.db import models

class Address(models.Model):
    class Meta:
        """ Spelling correction for admin page """
        verbose_name_plural = 'Address'

    street_name1 = models.CharField(max_length=254)
    street_name2 = models.CharField(max_length=254, blank=True)
    city = models.CharField(max_length=254)
    postcode = models.CharField(max_length=254)
    phone_number = models.CharField(max_length=12)

    def __str__(self):
            return self.street_name1 + ' ' + self.street_name2 