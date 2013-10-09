from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'autodocs.views.home', name='home'),
    # url(r'^autodocs/', include('autodocs.foo.urls')),
    url(r'^templates/', include('templates.urls', namespace='templates')),
    url(r'^generate/', include('generate.urls', namespace='generate')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
)
