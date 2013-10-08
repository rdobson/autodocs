from django.conf.urls import patterns, include, url

from templates import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'autodocs.views.home', name='home'),
    # url(r'^autodocs/', include('autodocs.foo.urls')),

    url(r'^$', views.IndexView.as_view(), name='index'),
)
