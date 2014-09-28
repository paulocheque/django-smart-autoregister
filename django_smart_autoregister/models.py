from django.conf import settings

import_models = getattr(settings, 'IMPORT_SMART_AUTOREGISTER_MODELS', False)

if settings.IMPORT_SMART_AUTOREGISTER_MODELS:
    from django_smart_autoregister.models_test import *
