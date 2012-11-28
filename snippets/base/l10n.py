# coding=utf-8
import codecs
import os
from collections import defaultdict

from django.conf import settings

from snippets.l10n_utils.dotlang import mail_error


def lang_file_path(lang):
    return os.path.join(settings.ROOT, 'locale', lang,
                        '{0}.lang'.format(settings.DOTLANG_FILE))


def extract_strings(modeladmin, request, queryset):
    # We extract item by item because each item has certain locales it will be
    # extracted to. This isn't the best performance-wise, but extracting a ton
    # of snippets at once should be rare anyway.
    for item in queryset:
        slug, new_strings = item.extract_translations()
        for locale in [l.locale for l in item.locale_set.all()]:
            merge_strings(locale, slug, new_strings)

    modeladmin.message_user(request, 'Strings extracted successfully.')
extract_strings.short_description = 'Extract strings from selected items'


def merge_strings(lang, slug, new_strings):
    path = lang_file_path(lang)

    # Create the file and directories if it doesn't exist.
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    open(path, 'a').close()

    translations = parse_snippets_lang_file(path)

    # Remove strings that are not in the new set of translations.
    for old_string in translations[slug].keys():
        if old_string not in new_strings:
            del translations[slug][old_string]

    # Add new strings that are not in the old set.
    for new_string in new_strings:
        if new_string not in translations[slug]:
            translations[slug][new_string] = new_string

    with codecs.open(path, 'w', 'utf-8', errors='replace') as f:
        for slug, t in translations.items():
            for source, trans in t.items():
                f.write('#{0}\n;{1}\n{2}\n\n'.format(slug, source, trans))


def parse_snippets_lang_file(path):
    """
    Parse a specially-formatted .lang file for the Snippets server.

    Each string should have a comment above it signifying the slug and type
    of object being translated. For example:

        #snippet-firefox
        ;This is my <a href="%s">my snippet</a>!
        This is my <a href="%s">my snippet</a>!

        #template-simple
        ;A string in a template.
        A string in a template.
    """
    with codecs.open(path, 'r', 'utf-8', errors='replace') as lines:
        translations = defaultdict(dict)

        slug = None
        source = None
        for line in lines:
            if u'�' in line:
                mail_error(path, line)

            line = line.strip()
            if line == '':
                slug = None
                source = None
            elif line[0] == '#':
                slug = line[1:]
            elif line[0] == ';':
                source = line[1:]
            elif source and slug:
                translations[slug][source] = line.strip()

    return translations
