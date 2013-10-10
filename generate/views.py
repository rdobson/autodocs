# Create your views here.

from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
import jinja2

from articlegenerator.extract import *

from models import *
from templates.models import Template

REPO_BASE_LOC = '/tmp/'

def get_driver_repo_data_source(location):
    data_source = DriverRepoDataSource(REPO_BASE_LOC + location)
    data_source.collect()
    return data_source 

class PageCreate(generic.edit.CreateView):
    model = Page
    fields = ['name', 'location', 'template', 'xs_version', 'vendor_name',
              'supp_pack_guide_ctx']
    template_name_suffix = '_create'

class PageUpdate(generic.edit.UpdateView):
    model = Page
    fields = ['name', 'location', 'template']
    template_name_suffix = '_update'

class PageDelete(generic.edit.DeleteView):
    model = Page
    fields = ['name', 'location', 'template']
    template_name_suffix = '_check_delete'
    success_url = reverse_lazy('generate:page-list')

class PageList(generic.ListView):
    context_object_name = 'page_list'
        
    def get_queryset(self):
        return Page.objects.all()


class PageRender(generic.base.View):
    
    def get(self, request, pk):
        page = Page.objects.get(pk=pk)
        page_rec = { 
                        'xs_version'            : page.xs_version,
                        'vendor_name'           : page.vendor_name,
                        'supp_pack_guide_ctx'   : page.supp_pack_guide_ctx,
                        'hotfix_name'           : page.hotfix_name,
                        'hotfix_ctx'            : page.hotfix_ctx,
                        'original_ctx'          : page.original_ctx,
                   }
        page_data = ArticleDataSource(data=page_rec)
        repo_data = get_driver_repo_data_source(page.location)

        template = Template.objects.get(pk=page.template.pk)
        jinja_template = jinja2.Template(template.data)

        render_data = page_data + repo_data
        return HttpResponse(jinja_template.render(**render_data.export()))








