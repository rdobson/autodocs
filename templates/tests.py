"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from templates.models import *
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

class TemplateTests(TestCase):

    def setUp(self):
        self.template_str = "<html><body>Test Template with {{var}}.</body></html>"
        self.template_name = "Template 1"
    
    def test_get_content(self):
        """
        Tests that template object returns content correctly.
        """
        template = Template(name=self.template_name, data=self.template_str)
        self.assertEqual(template.get_content(), self.template_str)

    def test_get_name(self):
        """
        Test that ensure we return the templates name.
        """
        template = Template(name=self.template_name, data=self.template_str)
        self.assertEqual(template.get_name(), self.template_name)


################# View Tests ########################

def create_template(name, data):
    template = Template(name=name, data=data)
    template.save()
    return template

class TemplateIndexTests(TestCase):

    def test_template_name_appears_in_index(self):
        """
        Test that creating a new template makes its name appear in the
        index view of all the templates.
        """
        template_name = "Test Template 1"
        create_template(name=template_name, data="<html></html>")
        # Make the call
        response = self.client.get(reverse('templates:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, template_name)

