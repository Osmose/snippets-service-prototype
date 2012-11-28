from time import gmtime, strftime

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render
from django.utils import translation
from django.views.decorators.cache import cache_control

from commonware.response.decorators import xframe_allow

from snippets.base.decorators import access_control
from snippets.base.http import JSONResponse
from snippets.base.models import (Client, ClientMatchRule, Snippet,
                                  SnippetTemplate)
from snippets.base.utils import snippet_settings


HTTP_MAX_AGE = getattr(settings, 'SNIPPET_HTTP_MAX_AGE', 1)


@cache_control(public=True, max_age=HTTP_MAX_AGE)
def index(request):
    return render(request, 'base/index.html')


@cache_control(public=True, max_age=HTTP_MAX_AGE)
@access_control(max_age=HTTP_MAX_AGE)
def fetch_snippets(request, **kwargs):
    client = Client(**kwargs)
    translation.activate(client.locale)

    matching_snippets = Snippet.objects.match_client(client)
    snippet_ids = list(matching_snippets.values_list('id', flat=True))

    client_match_rules = ClientMatchRule.objects.filter(snippet__in=snippet_ids)
    passed_rules, failed_rules = client_match_rules.evaluate(client)

    matching_snippets = matching_snippets.exclude(
        client_match_rules__in=(list(failed_rules)))
    return render(request, 'base/fetch_snippets.html', {
        'snippets': matching_snippets,
        'snippet_settings': snippet_settings(),
        'current_time': strftime('%Y-%m-%dT%H:%M:%SZ', gmtime())
    })


@staff_member_required
def admin_template_json(request, template_id):
    """Retrieve a snippet template and return it in JSON form."""
    template = get_object_or_404(SnippetTemplate, id=template_id)
    return JSONResponse({
        'code': template.code,
        'fields': [{'name': var.name, 'type': var.type} for var in
                   template.variable_set.all()]
    })


def preview_snippet(request, snippet_id):
    snippet = get_object_or_404(Snippet, id=snippet_id)
    return render(request, 'base/preview.html', {
        'snippet': snippet,
        'snippet_settings': snippet_settings()
    })


@staff_member_required
@xframe_allow
def preview_empty(request):
    return render(request, 'base/preview_empty.html',
                  {'snippet_settings': snippet_settings()})
