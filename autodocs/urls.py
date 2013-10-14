from django.conf.urls import patterns, include, url
from autodocs.views import HomeView
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', HomeView.as_view(), name='home'),
    # url(r'^autodocs/', include('autodocs.foo.urls')),
    url(r'^templates/', include('templates.urls', namespace='templates')),
    url(r'^articles/', include('articles.urls', namespace='articles')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
)
