from django.conf import settings
from django.shortcuts import render
from django.views.decorators.cache import cache_control


HTTP_MAX_AGE = getattr(settings, 'SNIPPET_HTTP_MAX_AGE', 1)


@cache_control(public=True, max_age=HTTP_MAX_AGE)
def index(request):
    return render(request, 'base/index.html')
