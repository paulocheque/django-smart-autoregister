IMPORT_SMART_AUTOREGISTER_MODELS = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

SECRET_KEY = 'dsa-secret-key'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',

    'django_coverage',
    'django_nose',
    'django_smart_autoregister',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_PLUGINS = []

# Tell nose to measure coverage on the 'foo' and 'bar' apps
NOSE_ARGS = [
    '--with-coverage',
    '--cover-html',
    '--cover-package=django_smart_autoregister',
    '--cover-tests',
    '--cover-erase',
    ]

# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = '/tmp/invest-messages'  # change this to a proper location
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# To avoid warnings
MIDDLEWARE_CLASSES = ()


ROOT_URLCONF = 'urls'