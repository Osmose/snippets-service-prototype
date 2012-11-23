from django.db.models import Manager
from django.db.models.query import QuerySet


class SnippetManager(Manager):
    def match_client(self, client):
        from snippets.base.models import CHANNELS, STARTPAGE_VERSIONS

        # Retrieve the first item that starts with an available item. Allows
        # things like "release-cck-mozilla14" to match "release".
        client_channel = next(channel for channel in CHANNELS if
                              client.channel.startswith(channel))
        client_startpage_version = next(
            version for version in STARTPAGE_VERSIONS if
            client.startpage_version.startswith(version))

        return self.filter(**{
            'on_{0}'.format(client_channel): True,
            'on_startpage_{0}'.format(client_startpage_version): True,
            'product_name': client.name
        })


class ClientMatchRuleQuerySet(QuerySet):
    def evaluate(self, client):
        passed_rules, failed_rules = [], []
        for rule in self:
            if rule.evaluate(client):
                passed_rules.append(rule)
            else:
                failed_rules.append(rule)
        return passed_rules, failed_rules


class ClientMatchRuleManager(Manager):
    def get_query_set(self):
        return ClientMatchRuleQuerySet(self.model)
