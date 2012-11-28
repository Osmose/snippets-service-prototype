import json
import re
from collections import namedtuple

from django.conf import settings
from django.db import models
from django.utils import translation

from jingo import env
from jinja2 import Markup
from product_details import product_details

from snippets.base.managers import ClientMatchRuleManager, SnippetManager


CHANNELS = ('release', 'beta', 'aurora', 'nightly')
STARTPAGE_VERSIONS = ('1', '2', '3')

ENGLISH_LANGUAGE_CHOICES = sorted(
    [(key.lower(), u'{0} ({1})'.format(key, value['English']))
     for key, value in product_details.languages.items()]
)


Client = namedtuple('Client', ('startpage_version', 'name', 'version',
                               'appbuildid', 'build_target', 'locale',
                               'channel', 'os_version', 'distribution',
                               'distribution_version'))


class LocaleField(models.CharField):
    description = ('CharField with locale settings specific to Snippets '
                   'defaults.')

    def __init__(self, max_length=32, default=settings.LANGUAGE_CODE,
                 choices=ENGLISH_LANGUAGE_CHOICES, *args, **kwargs):
        return super(LocaleField, self).__init__(
            max_length=max_length, default=default, choices=choices,
            *args, **kwargs)


class SnippetTemplate(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, null=True)
    code = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def extract_translations(self):
        """
        Return a slug and set of strings that need to be translated for this
        template.
        """
        slug = 'template-{0}'.format(self.slug)
        translations = [msg for lineno, func, msg in
                        env.extract_translations(self.code) if msg]
        return slug, translations

    def __unicode__(self):
        return self.name


class SnippetTemplateVariable(models.Model):
    TEXT = 0
    IMAGE = 1
    LOCALIZED_TEXT = 2
    TYPE_CHOICES = ((TEXT, 'Text'), (LOCALIZED_TEXT, 'Localized Text'),
                    (IMAGE, 'Image'))

    template = models.ForeignKey(SnippetTemplate, related_name='variable_set')
    name = models.CharField(max_length=255)
    type = models.IntegerField(choices=TYPE_CHOICES, default=TEXT)

    def __unicode__(self):
        return u'{0}:{1}'.format(self.template.name, self.name)


class SnippetTemplateLocale(models.Model):
    template = models.ForeignKey(SnippetTemplate, related_name='locale_set')
    locale = LocaleField()


class ClientMatchRule(models.Model):
    description = models.CharField(max_length=255)
    exclusion = models.BooleanField(default=False)

    startpage_version = models.CharField(max_length=64, blank=True)
    name = models.CharField(max_length=64, blank=True)
    version = models.CharField(max_length=64, blank=True)
    appbuildid = models.CharField(max_length=64, blank=True)
    build_target = models.CharField(max_length=64, blank=True)
    locale = models.CharField(max_length=64, blank=True)
    channel = models.CharField(max_length=64, blank=True)
    os_version = models.CharField(max_length=64, blank=True)
    distribution = models.CharField(max_length=64, blank=True)
    distribution_version = models.CharField(max_length=64, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = ClientMatchRuleManager()

    def evaluate(self, client):
        match = True
        for field in client._fields:
            field_value = getattr(self, field, None)
            if not field_value:
                continue

            client_field_value = getattr(client, field)
            if field_value.startswith('/'):
                try:
                    if re.match(field_value[1:-1], client_field_value) is None:
                        match = False
                        break
                except re.error:
                    # TODO: Figure out better behavior here.
                    match = False
                    break
            elif field_value != client_field_value:
                match = False
                break

        if self.exclusion:
            return not match
        else:
            return match

    def __unicode__(self):
        return self.description


class Snippet(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, null=True)
    template = models.ForeignKey(SnippetTemplate)
    data = models.TextField(default='{}')

    # Matching fields
    product_name = models.CharField(max_length=255, default='Firefox')

    on_release = models.BooleanField(default=False, verbose_name='Release')
    on_beta = models.BooleanField(default=False, verbose_name='Beta')
    on_aurora = models.BooleanField(default=False, verbose_name='Aurora')
    on_nightly = models.BooleanField(default=False, verbose_name='Nightly')

    # Adding startpage here seems silly, but it changes so little and, more
    # importantly, lets us set defaults for all snippets, whereas a rule would
    # be more flexible but not auto-add without some magic.
    on_startpage_1 = models.BooleanField(default=False,
                                         verbose_name='Version 1')
    on_startpage_2 = models.BooleanField(default=True,
                                         verbose_name='Version 2')
    on_startpage_3 = models.BooleanField(default=True,
                                         verbose_name='Version 3')

    client_match_rules = models.ManyToManyField(
        ClientMatchRule, blank=True, verbose_name='Client Match Rules')

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = SnippetManager()

    def render(self, locale=None):
        current_langauge = False
        if locale:
            current_langauge = translation.get_language()
            translation.activate(locale)

        data = dict([(name, Markup(item['value'])) for name, item in
                     json.loads(self.data).items()])

        rendered_snippet = '<div data-snippet-id="{0}">{1}</div>'.format(
            self.id, env.from_string(self.template.code).render(data))

        if current_langauge:
            translation.activate(current_langauge)
        return Markup(rendered_snippet)

    def match_client(self, client):
        if not getattr(self, 'on_{0}'.format(client.channel), False):
            return False

        startpage_key = 'on_startpage_{0}'.format(client.startpage_version)
        if not getattr(self, startpage_key, False):
            return False

        if not self.product_name == client.name:
            return False

        return True

    def extract_translations(self):
        """
        Return a slug and set of strings that need to be translated for this
        snippet.
        """
        slug = 'snippet-{0}'.format(self.slug)
        data = json.loads(self.data)

        translations = [item['value'] for key, item in data.items() if
                        item['type'] == SnippetTemplateVariable.LOCALIZED_TEXT]
        return slug, translations

    def __unicode__(self):
        return self.name


class SnippetLocale(models.Model):
    template = models.ForeignKey(Snippet, related_name='locale_set')
    locale = LocaleField()


class SnippetSettings(models.Model):
    """
    Stores site-wide settings, such as the global snippet CSS and JS.

    There should only ever be one row in the database.
    """
    global_css = models.TextField()
    global_js = models.TextField()


# South introspection rules for LocaleField
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ['^snippets\.base\.models\.LocaleField'])
