from django.db import models
from django.core.urlresolvers import reverse


class Hotfix(models.Model): 
    name = models.CharField(max_length=50)
    version = models.CharField(max_length=15)
    ctx = models.CharField(max_length=10)

    def get_absolute_url(self):
        return reverse('hotfixes:hotfix_update', kwargs={'pk':self.pk})

    def __unicode__(self):
        return self.name
