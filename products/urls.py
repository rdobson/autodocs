from django.conf.urls import patterns, include, url

from products import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'autodocs.views.home', name='home'),
    # url(r'^autodocs/', include('autodocs.foo.urls')),

    url(r'^$', views.IndexView.as_view(), name='product-list'),
    url(r'add/$', views.ProductCreate.as_view(), name='product_create'),
    url(r'(?P<pk>\d+)/$', views.ProductUpdate.as_view(), name='product_update'),
    url(r'(?P<pk>\d+)/delete/$', views.ProductDelete.as_view(), name='product_delete'),
)
