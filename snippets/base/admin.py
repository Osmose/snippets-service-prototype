from django.contrib import admin
from django.db.models import Q

from jingo import env
from jinja2.meta import find_undeclared_variables

from snippets.base import models
from snippets.base.forms import SnippetAdminForm


class SnippetAdmin(admin.ModelAdmin):
    form = SnippetAdminForm
    list_display = ('name', 'template', 'channels', 'created', 'modified')
    list_filter = ('template', 'on_release', 'on_beta', 'on_aurora',
                   'on_nightly', 'client_match_rules')
    fieldsets = (
        (None, {'fields': ('name', 'template', 'data')}),
        ('Product Channels', {
            'description': 'What channels will this snippet be available in?',
            'fields': ('on_release', 'on_beta', 'on_aurora', 'on_nightly'),
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
admin.site.register(models.Snippet, SnippetAdmin)


class SnippetTemplateVariableInline(admin.TabularInline):
    model = models.SnippetTemplateVariable
    max_num = 0
    can_delete = False
    readonly_fields = ('name',)
    fields = ('name', 'type',)


class SnippetTemplateAdmin(admin.ModelAdmin):
    inlines = (SnippetTemplateVariableInline,)

    def save_related(self, request, form, formsets, change):
        """
        After saving the related objects, remove and add
        SnippetTemplateVariables depending on how the template code changed.
        """
        super(SnippetTemplateAdmin, self).save_related(request, form, formsets,
                                                       change)
        ast = env.parse(form.instance.code)
        new_vars = find_undeclared_variables(ast)
        var_manager = form.instance.snippettemplatevariable_set

        # Delete variables not in the new set.
        var_manager.filter(~Q(name__in=new_vars)).delete()

        # Create variables that don't exist.
        for variable in new_vars:
            var_manager.get_or_create(name=variable)
admin.site.register(models.SnippetTemplate, SnippetTemplateAdmin)


class ClientMatchRuleAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.ClientMatchRule, ClientMatchRuleAdmin)
