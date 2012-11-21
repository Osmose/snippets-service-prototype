from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import cache_control

from commonware.response.decorators import xframe_allow

from snippets.base.http import JSONResponse
from snippets.base.models import Snippet, SnippetTemplate
from snippets.base.utils import snippet_settings


HTTP_MAX_AGE = getattr(settings, 'SNIPPET_HTTP_MAX_AGE', 1)


@cache_control(public=True, max_age=HTTP_MAX_AGE)
def index(request):
    return render(request, 'base/index.html')


@staff_member_required
def admin_template_json(request, template_id):
    """Retrieve a snippet template and return it in JSON form."""
    template = get_object_or_404(SnippetTemplate, id=template_id)
    return JSONResponse({
        'code': template.code,
        'fields': [{'name': var.name, 'type': var.type} for var in
                   template.snippettemplatevariable_set.all()]
    })


@staff_member_required
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
