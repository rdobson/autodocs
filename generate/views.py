# Create your views here.

from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse

from articlegenerator.extract import *

from models import *

REPO_BASE_LOC = '/tmp/'

def get_driver_repo_data(location):
    data_source = DriverRepoDataSource(REPO_BASE_LOC + location)
    data_source.collect()
    return data_source.export() 

class PageCreate(generic.edit.CreateView):
    model = Page
    fields = ['name', 'location', 'template']
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
        data = get_driver_repo_data(page.location)

        return HttpResponse('Test: %s' % data)
