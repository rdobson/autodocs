# Create your views here.

from django.views import generic
from django.core.urlresolvers import reverse_lazy

from models import *

class TemplateCreate(generic.edit.CreateView):
    model = Template
    fields = ['name', 'data']
    template_name_suffix = '_create'

class TemplateUpdate(generic.edit.UpdateView):
    model = Template
    fields = ['name', 'data']
    template_name_suffix = '_update'
    
class TemplateDelete(generic.edit.DeleteView):
    model = Template
    fields = ['name', 'data']
    success_url = reverse_lazy('templates:template-list')
    template_name_suffix = '_check_delete'
    
class IndexView(generic.ListView):
    context_object_name = 'template_list'
    
    def get_queryset(self):
        """Return the list of available templates."""
        return Template.objects.all() 
        
