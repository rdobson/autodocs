from django.db import models
from django.core.exceptions import ValidationError

class Template(models.Model):
    name = models.CharField(max_length=200)
    data = models.TextField()

    def get_content(self):
        return self.data

    def get_name(self):
        return self.name

