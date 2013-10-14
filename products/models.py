from django.db import models
from django.core.urlresolvers import reverse


class Product(models.Model): 
    name = models.CharField(max_length=50)
    version = models.CharField(max_length=15)
    supp_pack_guide_ctx = models.CharField(max_length=10)

    def get_absolute_url(self):
        return reverse('products:product_update', kwargs={'pk':self.pk})

# Create your models here.
