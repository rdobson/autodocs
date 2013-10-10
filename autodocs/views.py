from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render_to_response

class HomeView(generic.base.View):
    
    def get(self, request):
        return render_to_response('base.html', {}) 
