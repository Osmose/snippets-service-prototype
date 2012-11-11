# This is your project's main settings file that can be committed to your
# repo. If you need to override a setting locally, use settings_local.py

from funfactory.settings_base import *

# Name of the top-level module where you put all your apps.
# If you did not install Playdoh with the funfactory installer script
# you may need to edit this value. See the docs about installing from a
# clone.
PROJECT_MODULE = 'snippets'

# Defines the views served for root URLs.
ROOT_URLCONF = '%s.urls' % PROJECT_MODULE

INSTALLED_APPS = list(INSTALLED_APPS) + [
    'snippets.base',

    'django.contrib.admin',

    'south',
]

LOCALE_PATHS = (
    os.path.join(ROOT, PROJECT_MODULE, 'locale'),
)

# Because Jinja2 is the default template loader, add any non-Jinja templated
# apps here:
JINGO_EXCLUDE_APPS = [
    'admin',
    'registration',
]

SITE_URL = 'http://localhost:8000'

# Tells the extract script what files to look for L10n in and what function
# handles the extraction. The Tower library expects this.
DOMAIN_METHODS['messages'] = [
    ('%s/**.py' % PROJECT_MODULE,
        'tower.management.commands.extract.extract_tower_python'),
    ('%s/**/templates/**.html' % PROJECT_MODULE,
        'tower.management.commands.extract.extract_tower_template'),
    ('templates/**.html',
        'tower.management.commands.extract.extract_tower_template'),
]

LOGGING = dict(loggers=dict(playdoh={'level': logging.DEBUG}))
