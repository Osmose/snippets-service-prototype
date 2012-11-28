from django.contrib import admin
from django.db.models import Q

from jingo import env, load_helpers
from jinja2.meta import find_undeclared_variables

from snippets.base import models
from snippets.base.forms import SnippetAdminForm, SnippetTemplateAdminForm
from snippets.base.l10n import extract_strings


class SnippetAdmin(admin.ModelAdmin):
    form = SnippetAdminForm
    prepopulated_fields = {'slug': ('name',)}
    actions = [extract_strings]
    list_display = ('name', 'template', 'channels', 'created', 'modified')
    list_filter = ('template', 'on_release', 'on_beta', 'on_aurora',
                   'on_nightly', 'client_match_rules')
    fieldsets = (
        (None, {'fields': ('name', 'slug', 'template', 'data')}),
        ('Product Channels', {
            'description': 'What channels will this snippet be available in?',
            'fields': ('on_release', 'on_beta', 'on_aurora', 'on_nightly'),
        }),
        ('Locales', {
            'description': ('Snippet only shown in locales that have been '
                            'fully translated.<br />Both the snippet '
                            '<strong>and</strong> the template must be '
                            'translated.'),
            'fields': ('locales',),

        }),
        ('Startpage Versions', {
            'classes': ('collapse',),
            'fields': ('on_startpage_1', 'on_startpage_2', 'on_startpage_3'),
        }),
        ('Extra', {
            'classes': ('collapse',),
            'fields': ('product_name', 'client_match_rules'),
        })
    )

    def channels(self, instance):
        channels = []
        for channel in ['release', 'beta', 'aurora', 'nightly']:
            if getattr(instance, 'on_{0}'.format(channel), False):
                channels.append(channel)
        return ', '.join(channels)

    def save_model(self, request, obj, form, change):
        """Save locale changes as well as the snippet itself."""
        super(SnippetAdmin, self).save_model(request, obj, form, change)

        locales = form.cleaned_data['locales']
        obj.locale_set.all().delete()
        for locale in locales:
            models.SnippetLocale.objects.create(template=obj, locale=locale)
admin.site.register(models.Snippet, SnippetAdmin)


class SnippetTemplateVariableInline(admin.TabularInline):
    model = models.SnippetTemplateVariable
    max_num = 0
    can_delete = False
    readonly_fields = ('name',)
    fields = ('name', 'type',)


RESERVED_VARIABLES = ('_',)


class SnippetTemplateAdmin(admin.ModelAdmin):
    inlines = (SnippetTemplateVariableInline,)
    prepopulated_fields = {'slug': ('name',)}
    actions = [extract_strings]
    form = SnippetTemplateAdminForm

    def save_model(self, request, obj, form, change):
        """Save locale changes as well as the template itself."""
        super(SnippetTemplateAdmin, self).save_model(request, obj, form, change)

        locales = form.cleaned_data['locales']
        obj.locale_set.all().delete()
        for locale in locales:
            models.SnippetTemplateLocale.objects.create(template=obj,
                                                        locale=locale)

    def save_related(self, request, form, formsets, change):
        """
        After saving the related objects, remove and add
        SnippetTemplateVariables depending on how the template code changed.
        """
        super(SnippetTemplateAdmin, self).save_related(request, form, formsets,
                                                       change)
        load_helpers()  # Ensure jingo helpers are loaded.
        ast = env.parse(form.instance.code)
        new_vars = find_undeclared_variables(ast)
        var_manager = form.instance.variable_set

        # Filter out reserved variable names.
        new_vars = filter(lambda x: not x in RESERVED_VARIABLES, new_vars)

        # Delete variables not in the new set.
        var_manager.filter(~Q(name__in=new_vars)).delete()

        # Create variables that don't exist.
        for variable in new_vars:
            var_manager.get_or_create(name=variable)
admin.site.register(models.SnippetTemplate, SnippetTemplateAdmin)


class ClientMatchRuleAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.ClientMatchRule, ClientMatchRuleAdmin)
