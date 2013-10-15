"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models import *
from views import *
from templates.models import Template
from products.models import Product
from hotfixes.models import Hotfix
from django.core.urlresolvers import reverse


class ModelUtilFunctions(TestCase):
    
    def test_get_model_attributes(self):
        
        class Test(object):
            x = 2
            y = 5

        obj_inst = Test()
        attrs = get_model_attributes(obj_inst)
        assert(len(attrs) == 2)
        assert('x' in attrs and 'y' in attrs)

    def test_model_to_datasource(self):
        product = Product.objects.create(name='XenServer 6.1',
                                         version='6.1',
                                         supp_pack_guide_ctx='CTX12542')

        rec = model_to_datasource(product)
        assert(rec['product_name'] == 'XenServer 6.1')
        assert(rec['product_version'] == '6.1')
        assert(rec['product_supp_pack_guide_ctx'] == 'CTX12542')


class ArticleModelTests(TestCase):

    def test_article_create(self):
        template = Template.objects.create(name='Test Template', data='<html></html>')
        product = Product.objects.create(name='XenServer 6.1', 
                                         version='6.1', 
                                         supp_pack_guide_ctx='CTX12542')  
        hotfix = Hotfix.objects.create(name='Blah',
                                       version='HFX602E01',
                                       ctx='CTX23523')
        page = Article.objects.create(location='blah', 
                                      template=template,
                                      product=product,
                                      hotfix=hotfix)


class ArticlesViewTests(TestCase):

    def test_article_create_view_expect_200(self):
        response = self.client.get(reverse('articles:article_create'))
        self.assertEqual(response.status_code, 200)
