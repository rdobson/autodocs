# Create your views here.

from django.views import generic
from django.core.urlresolvers import reverse_lazy

from models import *

class HotfixCreate(generic.edit.CreateView):
    model = Hotfix
    fields = ['name', 'version']
    template_name_suffix = '_create'

class HotfixUpdate(generic.edit.UpdateView):
    model = Hotfix
    fields = ['name', 'version']
    template_name_suffix = '_update'
    
class HotfixDelete(generic.edit.DeleteView):
    model = Hotfix
    fields = ['name', 'version']
    success_url = reverse_lazy('hotfixes:hotfix-list')
    template_name_suffix = '_check_delete'
    
class IndexView(generic.ListView):
    context_object_name = 'hotfix_list'
    
    def get_queryset(self):
        """Return the list of available templates."""
        return Hotfix.objects.all() 
        
