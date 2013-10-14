from django.db import models
from django.core.urlresolvers import reverse

class Article(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    template = models.ForeignKey('templates.Template')

    # Attributes needed
    xs_version = models.CharField(max_length=10)
    vendor_name = models.CharField(max_length=100)
    supp_pack_guide_ctx = models.CharField(max_length=10)

    # Just for hotfixes
    hotfix_name = models.CharField(max_length=20, blank=True)
    hotfix_ctx = models.CharField(max_length=10, blank=True)
    original_ctx = models.CharField(max_length=10, blank=True)

    def get_absolute_url(self):
        return reverse('articles:article_update', kwargs={'pk':self.pk})

    def __unicode__(self):
        return self.name

# Create your models here.
