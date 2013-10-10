from django.conf.urls import patterns, include, url

from generate import views

urlpatterns = patterns('',
    
    url(r'^$', views.PageList.as_view(), name='page-list'),
    url(r'(?P<pk>\d+)/render/$', views.PageRender.as_view(), name='page-render'),

    url(r'add/$', views.PageCreate.as_view(), name='page_create'),
    url(r'(?P<pk>\d+)/$', views.PageUpdate.as_view(), name='page_update'),
    url(r'(?P<pk>\d+)/delete/$', views.PageDelete.as_view(), name='page_delete'),
)
