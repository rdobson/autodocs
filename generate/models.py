from django.db import models

class Page(models.Model):
    location = models.CharField(max_length=200)
    template = models.ForeignKey('templates.Template')

# Create your models here.
