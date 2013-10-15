from django.db import models
from django.core.urlresolvers import reverse

class Article(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    template = models.ForeignKey('templates.Template')

    # Attributes needed
    vendor_name = models.CharField(max_length=100)
    product = models.ForeignKey('products.Product')

    # Just for hotfixes
    hotfix = models.ForeignKey('hotfixes.Hotfix')
    original_ctx = models.CharField(max_length=15)

    def get_absolute_url(self):
        return reverse('articles:article_update', kwargs={'pk':self.pk})

    def __unicode__(self):
        return self.name

# Create your models here.
