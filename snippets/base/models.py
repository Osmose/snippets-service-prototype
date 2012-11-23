import json
import re
from collections import namedtuple

from django.db import models

from jingo import env
from jinja2 import Markup

from snippets.base.managers import ClientMatchRuleManager, SnippetManager


CHANNELS = ('release', 'beta', 'aurora', 'nightly')
STARTPAGE_VERSIONS = ('1', '2', '3')


Client = namedtuple('Client', ('startpage_version', 'name', 'version',
                               'appbuildid', 'build_target', 'locale',
                               'channel', 'os_version', 'distribution',
                               'distribution_version'))


class SnippetTemplate(models.Model):
    name = models.CharField(max_length=255)
    code = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class SnippetTemplateVariable(models.Model):
    TEXT = 0
    IMAGE = 1
    TYPE_CHOICES = ((TEXT, 'Text'), (IMAGE, 'Image'))

    template = models.ForeignKey(SnippetTemplate)
    name = models.CharField(max_length=255)
    type = models.IntegerField(choices=TYPE_CHOICES, default=TEXT)

    def __unicode__(self):
        return u'{0}:{1}'.format(self.template.name, self.name)


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
    name = models.CharField(max_length=255)
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

    def render(self):
        data = dict([(name, Markup(item['value'])) for name, item in
                     json.loads(self.data).items()])

        rendered_snippet = '<div data-snippet-id="{0}">{1}</div>'.format(
            self.id, env.from_string(self.template.code).render(data))
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

    def __unicode__(self):
        return self.name


class SnippetSettings(models.Model):
    """
    Stores site-wide settings, such as the global snippet CSS and JS.

    There should only ever be one row in the database.
    """
    global_css = models.TextField()
    global_js = models.TextField()
