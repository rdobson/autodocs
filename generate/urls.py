from django.conf.urls import patterns, include, url

from generate import views

urlpatterns = patterns('',
    
    url(r'add/$', views.PageCreate.as_view(), name='page_create'),

)
