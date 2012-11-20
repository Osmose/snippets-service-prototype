from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import cache_control

from snippets.base.http import JSONResponse
from snippets.base.models import SnippetTemplate


HTTP_MAX_AGE = getattr(settings, 'SNIPPET_HTTP_MAX_AGE', 1)


@cache_control(public=True, max_age=HTTP_MAX_AGE)
def index(request):
    return render(request, 'base/index.html')


@staff_member_required
def admin_template_fields(request, template_id):
    """
    Retrieve the fields for an admin template and return them as a JSON blob.
    """
    template = get_object_or_404(SnippetTemplate, id=template_id)
    fields = [{'name': var.name, 'type': var.type} for var in
              template.snippettemplatevariable_set.all()]
    return JSONResponse(fields)
