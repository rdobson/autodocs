# Create your views here.

from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render_to_response
import jinja2

from articlegenerator.extract import *

from models import *
from templates.models import Template

REPO_BASE_LOC = '/tmp/'

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
        if type(vals) == type(unicode()):
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
    success_url = reverse_lazy('generate:article-list')

class ArticleList(generic.ListView):
    context_object_name = 'article_list'
        
    def get_queryset(self):
        return Article.objects.all()


class ArticleRender(generic.base.View):
    
    def get(self, request, pk):
        article = Article.objects.get(pk=pk)
        article_rec = { 
                        'xs_version'            : article.xs_version,
                        'vendor_name'           : article.vendor_name,
                        'supp_pack_guide_ctx'   : article.supp_pack_guide_ctx,
                        'hotfix_name'           : article.hotfix_name,
                        'hotfix_ctx'            : article.hotfix_ctx,
                        'original_ctx'          : article.original_ctx,
                   }
        article_data = ArticleDataSource(data=article_rec)
        repo_data = get_driver_repo_data_source(article.location)

        template = Template.objects.get(pk=article.template.pk)
        jinja_template = jinja2.Template(template.data)

        render_data = article_data + repo_data

        if request.GET.get('raw_data',False):
            return HttpResponse(str(describe_datasource(render_data)))

        if request.GET.get('show_data',False):
            describe_data = describe_datasource(render_data)
            return render_to_response('generate/describe_datasource.html',
                                        {'attributes': describe_data})

        return HttpResponse(jinja_template.render(**render_data.export()))








