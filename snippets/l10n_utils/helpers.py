import jingo
import jinja2

from django.conf import settings

from snippets.l10n_utils.dotlang import translate


def install_lang_files(ctx):
    """Install the initial set of .lang files"""
    req = ctx['request']

    if not hasattr(req, 'langfiles'):
        files = list(settings.DOTLANG_FILES)
        if ctx.get('langfile'):
            files.append(ctx.get('langfile'))
        setattr(req, 'langfiles', files)


def add_lang_files(ctx, files):
    """Install additional .lang files"""
    req = ctx['request']

    if hasattr(req, 'langfiles'):
        req.langfiles = files + req.langfiles


# TODO: make an ngettext compatible function. The pluaralize clause of a
# trans block won't work untill we do.
def gettext(text):
    """
    Translate a string, loading the translations for the locale if
    necessary.
    """
    trans = translate(text, settings.DOTLANG_FILES)
    return jinja2.Markup(trans)


@jingo.register.function
@jinja2.contextfunction
def lang_files(ctx, *files):
    """Add more lang files to the translation object"""
    # Filter out empty files
    install_lang_files(ctx)
    add_lang_files(ctx, [f for f in files if f])


# Install gettext into jinja2
jingo.env.install_gettext_callables(gettext, gettext)
