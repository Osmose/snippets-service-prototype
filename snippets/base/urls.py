from django.conf.urls.defaults import patterns, url

from snippets.base import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='base.index'),
    url(r'^admin/base/snippettemplate/(\d+)/variables/',
        views.admin_template_fields, name='base.admin.template_variables'),
)
