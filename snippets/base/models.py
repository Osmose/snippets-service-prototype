import json

from django.db import models

from jingo import env


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


class Snippet(models.Model):
    name = models.CharField(max_length=255)
    template = models.ForeignKey(SnippetTemplate)
    data = models.TextField(default='{}')

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def render(self):
        data = dict([(name, item['value']) for name, item in
                     json.loads(self.data).items()])
        return env.from_string(self.template.code).render(data)

    def __unicode__(self):
        return self.name


class ClientMatchRule(models.Model):
    description = models.CharField(max_length=255)

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

    def __unicode__(self):
        return self.description
