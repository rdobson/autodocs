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
import tempfile
import os

AKAMAI_BASE = "http://downloadns.citrix.com.edgesuite.net"


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


    def test_parse_source_path_fs_loc(self):
        fs_loc = "sanibel-lcm/driverdisks.hg/ixgbe-3.12.6/kb-CTX137591-2.6.32.12-0.7.1.xs6.0.2.553.170674xen"

        sanitised_loc = parse_source_path(fs_loc)
        self.assertEqual(sanitised_loc, fs_loc)


    def test_parse_source_path_fs_loc_carbon(self):
        fs_loc = "carbon/tampa-lcm/driverdisks.hg/tg3-3.131d/kb-CTX137629-2.6.32.43-0.4.1.xs1.6.10.777.170770xen"
        fs_path = "tampa-lcm/driverdisks.hg/tg3-3.131d/kb-CTX137629-2.6.32.43-0.4.1.xs1.6.10.777.170770xen"

        sanitised_loc = parse_source_path(fs_loc)
        self.assertEqual(sanitised_loc, fs_path)

    def test_parse_source_path_hg_web_url_ctx(self):
        web_url = "http://hg.uk.xensource.com/carbon/tampa-lcm/driverdisks.hg/file/090a8ce2d2cf/fnic-1.5.0.45/kb-CTX138993-2.6.32.43-0.4.1.xs1.6.10.784.170772xen"
        fs_path = "tampa-lcm/driverdisks.hg/fnic-1.5.0.45/kb-CTX138993-2.6.32.43-0.4.1.xs1.6.10.784.170772xen"

        sanitised_loc = parse_source_path(web_url)

    def test_parse_source_path_web_url_tracker(self):
        web_url = "http://hg.uk.xensource.com/carbon/tampa-lcm/driverdisks.hg/file/7f5084f7e8a8/aacraid-1.2.1/kb-CTX139297-2.6.32.43-0.4.1.xs1.6.10.734.170748xen"
        fs_path = "tampa-lcm/driverdisks.hg/aacraid-1.2.1/kb-CTX139297-2.6.32.43-0.4.1.xs1.6.10.734.170748xen"
        
        sanitised_loc = parse_source_path(web_url)
        self.assertEqual(sanitised_loc, fs_path)

    def test_get_akamai_url(self):
        zip_loc = "QL-196-GA-2.6.32.43-0.4.1.xs1.6.10.734.170748xen/qla2xxx-8.06.00.10.55.6-k-GA.zip"
        url = get_akamai_url(zip_loc)
        self.assertEqual(url, '%s/8460/qla2xxx-8.06.00.10.55.6-k-GA.zip' % AKAMAI_BASE)

    def test_get_akamai_data_source(self):
        rec = {
                'article_location': 'http://hg.uk.xensource.com/carbon/tampa-lcm/driverdisks.hg/file/6d4bb42877b2/qla2xxx-8.06.00.10.55.6-k/QL-196-GA-2.6.32.43-0.4.1.xs1.6.10.734.170748xen',
                'zip': {'filename': 'qla2xxx-8.06.00.10.55.6-k-GA.zip'},
              }

        ds = get_akamai_data_source(rec)
        self.assertEqual(ds.export()['akamai_zip_url'], '%s/8460/qla2xxx-8.06.00.10.55.6-k-GA.zip' % AKAMAI_BASE)


    def test_get_akamai_url_from_duplicate_list(self):
        akamai_log_line = "2014-01-24 16:10:45+00:00 http://downloadns.citrix.com.edgesuite.net/8763/fnic-1.6.0.6-XS61E035.zip /usr/groups/sources/HG/carbon/tampa-lcm/driverdisks.hg/fnic-1.6.0.6/CIS-167-XS61E035-2.6.32.43-0.4.1.xs1.6.10.794.170782xen/fnic-1.6.0.6-XS61E035.zip"
        zip_loc = "CIS-167-XS61E035-2.6.32.43-0.4.1.xs1.6.10.794.170782xen/fnic-1.6.0.6-XS61E035.zip"
        tmp_file = tempfile.NamedTemporaryFile(delete=False)
        tmp_file.write('\n'.join([akamai_log_line, akamai_log_line]))
        tmp_file.close()
        url = get_akamai_url(zip_loc, akamai_logs=tmp_file.name)
        self.assertEqual(url, 'http://downloadns.citrix.com.edgesuite.net/8763/fnic-1.6.0.6-XS61E035.zip')
        os.unlink(tmp_file.name)


class ArticleModelTests(TestCase):

    def test_article_create(self):
        template = Template.objects.create(name='Test Template', data='<html></html>')
        product = Product.objects.create(name='XenServer 6.1', 
                                         version='6.1', 
                                         supp_pack_guide_ctx='CTX12542')  
        hotfix = Hotfix.objects.create(name='Blah',
                                       version='HFX602E01',
                                       ctx='CTX23523',
                                       product=product)
        page = Article.objects.create(location='blah', 
                                      template=template,
                                      product=product,
                                      hotfix=hotfix)


class ArticlesViewTests(TestCase):

    def test_article_create_view_expect_200(self):
        response = self.client.get(reverse('articles:article_create'))
        self.assertEqual(response.status_code, 200)

