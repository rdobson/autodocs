"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models import *
from templates.models import Template

class PageModelTests(TestCase):

    def test_page_create(self):
        template = Template.objects.create(name='Test Template', data='<html></html>')
        page = Page.objects.create(location='blah', template=template)

