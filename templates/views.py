# Create your views here.

from django.views import generic
from models import *

class IndexView(generic.ListView):
    template_name = 'list.html'
    context_object_name = 'template_list'
    
    def get_queryset(self):
        """Return the list of available templates."""
        return Template.objects.all() 
        
