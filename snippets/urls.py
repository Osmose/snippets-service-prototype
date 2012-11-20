from django.conf import settings
from django.conf.urls.defaults import patterns, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from funfactory.admin import monkeypatch as admin_patch
from funfactory.monkeypatches import patch


# Funfactory monkey patches
patch()
admin_patch()

# Enable admin interface.
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'', include('snippets.base.urls')),
    (r'^admin/', include(admin.site.urls)),
)

## In DEBUG mode, serve media files through Django.
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
