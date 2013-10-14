from django.conf.urls import patterns, include, url

from hotfixes import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'autodocs.views.home', name='home'),
    # url(r'^autodocs/', include('autodocs.foo.urls')),

    url(r'^$', views.IndexView.as_view(), name='hotfix-list'),
    url(r'add/$', views.HotfixCreate.as_view(), name='hotfix_create'),
    url(r'(?P<pk>\d+)/$', views.HotfixUpdate.as_view(), name='hotfix_update'),
    url(r'(?P<pk>\d+)/delete/$', views.HotfixDelete.as_view(), name='hotfix_delete'),
)
