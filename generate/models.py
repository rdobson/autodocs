from django.db import models
from django.core.urlresolvers import reverse

class Page(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    template = models.ForeignKey('templates.Template')

    def get_absolute_url(self):
        return reverse('generate:page_update', kwargs={'pk':self.pk})

    def __unicode__(self):
        return self.name

# Create your models here.
