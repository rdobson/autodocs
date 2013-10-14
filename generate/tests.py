"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models import *
from templates.models import Template
from django.core.urlresolvers import reverse

class ArticleModelTests(TestCase):

    def test_article_create(self):
        template = Template.objects.create(name='Test Template', data='<html></html>')
        page = Article.objects.create(location='blah', template=template)


class GenerateViewTests(TestCase):

    def test_article_create_view_expect_200(self):
        response = self.client.get(reverse('generate:article_create'))
        self.assertEqual(response.status_code, 200)
