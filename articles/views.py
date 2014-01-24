# Create your views here.

from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render_to_response
import jinja2

from articlegenerator.extract import *

from models import *
from templates.models import Template
from products.models import Product
from hotfixes.models import Hotfix
import re
from os.path import basename

REPO_BASE_LOC = '/repos/'
AKAMAI_LOGS = '/home/xenbuild/xs-logs/akamai/uploads'

def get_driver_repo_data_source(location):
    data_source = DriverRepoDataSource(REPO_BASE_LOC + location)
    data_source.collect()
    return data_source

def describe_datasource(datasource):
    """
    Convert the contents of a data_source into a list of lists for attrs.

    Each param should contain:
    - Group
        [ name, value ]

    """    
    rec = datasource.export()
    def recurse_values(key, vals):
        res = []
        if type(vals) in [type(unicode()), type(str())]:
            # String
            res.append({'name': key, 'value': vals})
        elif type(vals) == type({}):
            # Dictionary
            for k, v in vals.iteritems():
                if key:
                    key_str = "%s.%s" % (key, k)
                else:
                    key_str = k
                res.append({'name': key_str, 'value': v})
        elif type(vals) == type([]):
            # List
            mlist = []
            for val in vals:
                mlist.append(recurse_values(None, val))
            
            rec = {'name': key, 'value': mlist, 'group':True}
            res.append(rec)
        return res

    res = []
    for k, v in rec.iteritems():
        res.extend(recurse_values(k, v))
    return res
        


class ArticleCreate(generic.edit.CreateView):
    model = Article
    fields = ['name', 'location', 'template', 'xs_version', 'vendor_name',
              'supp_pack_guide_ctx']
    template_name_suffix = '_create'

class ArticleUpdate(generic.edit.UpdateView):
    model = Article
    fields = ['name', 'location', 'template']
    template_name_suffix = '_update'

class ArticleDelete(generic.edit.DeleteView):
    model = Article
    fields = ['name', 'location', 'template']
    template_name_suffix = '_check_delete'
    success_url = reverse_lazy('articles:article-list')

class ArticleList(generic.ListView):
    context_object_name = 'article_list'
        
    def get_queryset(self):
        return Article.objects.all().order_by('-updated_at')


def get_model_attributes(model_inst):
    """
    Return the list of attribute names of a Django model.
    """
    attrs = [i for i in dir(model_inst) if not i.startswith('__')]
    return attrs


def model_to_datasource(model_inst):
    """
    Take a Django model instance, and return a datasource
    that can be used to populate an article.
    """
    rec = {}
    fields = model_inst._meta.fields
    for field in fields:
        field_key = "%s_%s" % (model_inst.__class__.__name__.lower(), field.name)
        rec[field_key] = getattr(model_inst, field.name)
    return rec

def parse_source_path(loc):
    """
    Take a location (as supplied by the user), and convert it to the
    source path that should be used to access the repo. In particular
    this function allows the user to specify either the source path,
    or the HG web URL - and we will convert as required.
    """

    hg_url_regex = 'http://hg.uk.xensource.com/carbon/(?P<branch>[\w\-]*)/driverdisks.hg/file/[0-9a-f]{12}/(?P<path>[\w\.\-\/]*$)'
    regex = re.compile(hg_url_regex)
    match = regex.match(loc)

    if match:
        # We've matched a web URL
        fs_path = "%s/driverdisks.hg/%s" % (match.group('branch'), 
                                            match.group('path'))
        return fs_path

    if loc.startswith('carbon/'):
        # Catch the case where the carbon dir has been included.
        # This is not required.
        return loc.replace('carbon/','')

    return loc

def get_akamai_url(zip_file, akamai_logs=AKAMAI_LOGS):
    """
    Take a driver repo location and attempt to find 
    """
    fh = open(akamai_logs,'r')
    lines = fh.readlines()
    fh.close()
    res = []
    for line in lines:
        date, time, akamai_url, zip_file_path = line.split()
        if zip_file in zip_file_path:
            res.append(akamai_url)
    res = set(res) #Remove duplicates if in existence.
    if len(res) > 1:
        raise Exception("Error: more than one match for %s: %s" % (zip_file, res))
    if res:
        return res.pop()
    else:
        return None

def get_akamai_data_source(data_rec):
    zip_loc = "%s/%s" % (basename(data_rec['article_location']), data_rec['zip']['filename'])
    akamai_rec = {}
    akamai_rec['akamai_zip_url'] = get_akamai_url(zip_loc)
    return ArticleDataSource(data=akamai_rec)

class ArticleRender(generic.base.View):
    
    def get(self, request, pk):
        article = Article.objects.get(pk=pk)
        models = [article, article.product, article.hotfix]

        ds = ArticleDataSource()
        for model in models:
            if model:
                data_rec = model_to_datasource(model)
                ds = ds + ArticleDataSource(data=data_rec)

        source_path = parse_source_path(article.location)
        ds = ds + get_driver_repo_data_source(source_path)
        ds = ds + get_akamai_data_source(ds.export())

        template = Template.objects.get(pk=article.template.pk)
        jinja_template = jinja2.Template(template.data)

        if request.GET.get('raw_data',False):
            return HttpResponse(str(describe_datasource(ds)))

        if request.GET.get('show_data',False):
            describe_data = describe_datasource(ds)
            return render_to_response('articles/describe_datasource.html',
                                        {'attributes': describe_data})

        return HttpResponse(jinja_template.render(**ds.export()))








