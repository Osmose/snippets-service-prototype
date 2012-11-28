from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.safestring import mark_safe

from jingo import env

from snippets.base.models import (ENGLISH_LANGUAGE_CHOICES, Snippet,
                                  SnippetTemplate)


class TemplateDataWidget(forms.HiddenInput):
    def render(self, *args, **kwargs):
        hidden_input = super(TemplateDataWidget, self).render(*args, **kwargs)
        return mark_safe(env.get_template('base/template_widget.html').render({
            'hidden_input': hidden_input
        }))


class SnippetAdminForm(forms.ModelForm):
    template = forms.ModelChoiceField(SnippetTemplate.objects.all(),
                                      empty_label=None)
    locales = forms.MultipleChoiceField(
        required=False,
        choices=ENGLISH_LANGUAGE_CHOICES,
        widget=FilteredSelectMultiple('locales', is_stacked=False))

    class Meta:
        model = Snippet
        widgets = {
            'data': TemplateDataWidget
        }

    class Media:
        css = {
            'all': ('admin/css/template_widget.css',),
        }
        js = ('admin/js/jquery-1.8.3.min.js', 'admin/js/nunjucks-dev.js',
              'admin/js/template_widget.js',)

    def __init__(self, *args, **kwargs):
        super(SnippetAdminForm, self).__init__(*args, **kwargs)

        # Populates the list of locales from the snippet's existing values.
        locales = self.instance.locale_set.all()
        self.fields['locales'].initial = [l.locale for l in locales]


class SnippetTemplateAdminForm(forms.ModelForm):
    locales = forms.MultipleChoiceField(
        required=False,
        choices=ENGLISH_LANGUAGE_CHOICES,
        widget=FilteredSelectMultiple('locales', is_stacked=False))

    def __init__(self, *args, **kwargs):
        super(SnippetTemplateAdminForm, self).__init__(*args, **kwargs)

        # Populates the list of locales from the snippet template's existing
        # values.
        locales = self.instance.locale_set.all()
        self.fields['locales'].initial = [l.locale for l in locales]

    class Meta:
        model = SnippetTemplate
