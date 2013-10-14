from django.conf.urls import patterns, include, url

from articles import views

urlpatterns = patterns('',
    
    url(r'^$', views.ArticleList.as_view(), name='article-list'),
    url(r'(?P<pk>\d+)/render/$', views.ArticleRender.as_view(), name='article-render'),

    url(r'add/$', views.ArticleCreate.as_view(), name='article_create'),
    url(r'(?P<pk>\d+)/$', views.ArticleUpdate.as_view(), name='article_update'),
    url(r'(?P<pk>\d+)/delete/$', views.ArticleDelete.as_view(), name='article_delete'),
)
