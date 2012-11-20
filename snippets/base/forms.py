from django import forms
from django.utils.safestring import mark_safe

from jingo import env

from snippets.base.models import Snippet, SnippetTemplate


class TemplateDataWidget(forms.HiddenInput):
    def render(self, *args, **kwargs):
        hidden_input = super(TemplateDataWidget, self).render(*args, **kwargs)
        return mark_safe(env.get_template('admin/template_widget.html').render({
            'hidden_input': hidden_input
        }))


class SnippetAdminForm(forms.ModelForm):
    template = forms.ModelChoiceField(SnippetTemplate.objects.all(),
                                      empty_label=None)

    class Meta:
        model = Snippet
        widgets = {
            'data': TemplateDataWidget
        }

    class Media:
        js = ('admin/jquery-1.8.3.min.js', 'admin/nunjucks-dev.js',
              'admin/template_widget.js',)
