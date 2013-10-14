# Create your views here.

from django.views import generic
from django.core.urlresolvers import reverse_lazy

from models import *

class ProductCreate(generic.edit.CreateView):
    model = Product
    fields = ['name', 'version']
    template_name_suffix = '_create'

class ProductUpdate(generic.edit.UpdateView):
    model = Product
    fields = ['name', 'version']
    template_name_suffix = '_update'
    
class ProductDelete(generic.edit.DeleteView):
    model = Product
    fields = ['name', 'version']
    success_url = reverse_lazy('products:product-list')
    template_name_suffix = '_check_delete'
    
class IndexView(generic.ListView):
    context_object_name = 'product_list'
    
    def get_queryset(self):
        """Return the list of available templates."""
        return Product.objects.all() 
        
