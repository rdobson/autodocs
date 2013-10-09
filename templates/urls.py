from django.conf.urls import patterns, include, url

from templates import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'autodocs.views.home', name='home'),
    # url(r'^autodocs/', include('autodocs.foo.urls')),

    url(r'^$', views.IndexView.as_view(), name='template-list'),
    url(r'add/$', views.TemplateCreate.as_view(), name='template_create'),
    url(r'(?P<pk>\d+)/$', views.TemplateUpdate.as_view(), name='template_update'),
    url(r'(?P<pk>\d+)/delete/$', views.TemplateDelete.as_view(), name='template_delete'),
)
