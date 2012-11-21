from snippets.base.models import SnippetSettings


def snippet_settings():
    settings = SnippetSettings.objects.all()
    if len(settings) < 1:
        return None
    return settings[0]
