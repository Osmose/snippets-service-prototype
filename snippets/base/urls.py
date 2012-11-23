from django.conf.urls.defaults import patterns, url

from snippets.base import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='base.index'),

    url(r'^(?P<startpage_version>[^/]+)/(?P<name>[^/]+)/(?P<version>[^/]+)/'
        '(?P<appbuildid>[^/]+)/(?P<build_target>[^/]+)/(?P<locale>[^/]+)/'
        '(?P<channel>[^/]+)/(?P<os_version>[^/]+)/(?P<distribution>[^/]+)/'
        '(?P<distribution_version>[^/]+)/$', views.fetch_snippets,
        name='view_snippets'),

    url(r'^admin/base/snippet/preview/', views.preview_empty,
        name='base.admin.preview_empty'),
    url(r'^admin/base/snippet/(\d+)/preview/', views.preview_snippet,
        name='base.admin.preview_snippet'),
    url(r'^admin/base/snippettemplate/(\d+)/variables/',
        views.admin_template_json, name='base.admin.template_json'),
)
