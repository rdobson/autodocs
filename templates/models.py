from django.db import models
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

class Template(models.Model):
    name = models.CharField(max_length=200)
    data = models.TextField()

    def get_content(self):
        return self.data

    def get_name(self):
        return self.name

    def get_absolute_url(self):
        return reverse('templates:template_update', kwargs={'pk':self.pk})
