from django.db import models
from django.core.urlresolvers import reverse
from smart_selects.db_fields import ChainedForeignKey

from hotfixes.models import Hotfix

class Article(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    template = models.ForeignKey('templates.Template')

    # Attributes needed
    vendor_name = models.CharField(max_length=100)
    product = models.ForeignKey('products.Product')

    # Just for hotfixes
    # Use a chained field to allow for auto-drop-down.
    hotfix = ChainedForeignKey(
                                'hotfixes.Hotfix', chained_field='product', 
                                chained_model_field='product', 
                                show_all=False,
                                auto_choose=True
                              )
    original_ctx = models.CharField(max_length=15, blank=True, null=True)

    # Generic attributes
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def get_absolute_url(self):
        return reverse('articles:article_update', kwargs={'pk':self.pk})

    def __unicode__(self):
        return self.name

# Create your models here.
