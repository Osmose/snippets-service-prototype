from django.conf.urls.defaults import patterns, url

from snippets.base import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='base.index'),
    url(r'^admin/base/snippet/preview/', views.preview_empty,
        name='base.admin.preview_empty'),
    url(r'^admin/base/snippet/(\d+)/preview/', views.preview_snippet,
        name='base.admin.preview_snippet'),
    url(r'^admin/base/snippettemplate/(\d+)/variables/',
        views.admin_template_json, name='base.admin.template_json'),
)
