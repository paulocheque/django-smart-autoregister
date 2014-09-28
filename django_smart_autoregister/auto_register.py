from distutils.version import StrictVersion

from django.conf import settings
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.db.models import *

from .django_helper import *

ADMIN_FIELDS = [
    'fields',
    'exclude',
    'inlines',
    'list_display',
    'list_display_links',
    'list_editable',
    'list_filter',
    'list_max_show_all',
    'list_per_page',
    'list_select_related',
    'raw_id_fields',
    'search_fields',
    'actions',
    'actions_on_top',
    'actions_on_bottom',
    'actions_selection_counter',
    'date_hierarchy',
    'fieldsets',
    'filter_horizontal',
    'filter_vertical',
    'form',
    'formfield_overrides',
    'ordering',
    'paginator',
    'prepopulated_fields',
    'preserve_filters',
    'radio_fields',
    'readonly_fields',
    'show_full_result_count',
    'view_on_site',
]


def is_boolean(field):
    return isinstance(field, (BooleanField, NullBooleanField))

def is_string(field):
    return isinstance(field, (CharField, EmailField, IPAddressField, SlugField, URLField))

def is_number(field):
    return isinstance(field, (IntegerField, SmallIntegerField, PositiveIntegerField,
        PositiveSmallIntegerField, BigIntegerField, CommaSeparatedIntegerField, DecimalField, FloatField))

def is_datetime(field):
    return isinstance(field, (DateTimeField, DateField, TimeField))

def is_file(field):
    return isinstance(field, (FileField, FilePathField))

def is_binary(field):
    if StrictVersion(django.get_version()) >= StrictVersion('1.6'):
        return isinstance(field, (BinaryField))
    else:
        return False


def is_suitable_for_raw_id_fields(field):
    return is_relationship_field(field)

def is_suitable_for_list_display(field):
    return is_string(field) or is_boolean(field) or is_number(field) or is_datetime(field)

def is_suitable_for_list_filter(field):
    return field_has_choices(field) or is_boolean(field)

def is_suitable_for_list_display_links(field):
    return is_suitable_for_list_filter(field)

def is_suitable_for_search_fields(field):
    return is_string(field)


# function(field) => boolean
FIELD_STRATEGY = {
    'raw_id_fields': is_suitable_for_raw_id_fields,
    'list_display': is_suitable_for_list_display,
    'list_display_links': is_suitable_for_list_display_links,
    'list_filter': is_suitable_for_list_filter,
    'search_fields': is_suitable_for_search_fields,
    'list_per_page': 5,
    'list_max_show_all': 50
}


def confirm_list_display(value):
    if not value:
        return ['id', '__str__']
    if len(value) > 15:
        return value[0:15]
    return value

def confirm_list_display_links(value):
    return confirm_list_display(value)

def confirm_search_fields(value):
    if not value:
        return ['id']
    return value


# function(values) => values
FULL_STRATEGY = {
    'list_display': confirm_list_display,
    'list_display_links': confirm_list_display_links,
    'search_fields': confirm_search_fields,
}

def get_strategy(default, settings_name):
    strategy = {}
    strategy.update(default)
    if hasattr(settings, settings_name):
        print(getattr(settings, settings_name))
        strategy.update(getattr(settings, settings_name))
    return strategy

STRATEGY = get_strategy(FIELD_STRATEGY, 'DSA_FIELD_STRATEGY')
print(STRATEGY)
FINAL_STRATEGY = get_strategy(FULL_STRATEGY, 'DSA_FULL_STRATEGY')
print(FINAL_STRATEGY)


def register_admin_class(admin_class, override=False):
    try:
        admin.site.register(model, admin_class)
    except AlreadyRegistered:
        if override:
            admin.site.unregister(model)
            admin.site.register(model, admin_class)


def create_admin_inline_class(model, inline_class=admin.TabularInline):
    """
    admin.TabularInline or admin.StackedInline
    """
    attrs = {}
    attrs['model'] = model
    return type(get_model_name(model) + 'Inline', (inline_class,), attrs)


def create_admin_class(model, **kwargs):
    # print(get_model_name(model), kwargs)
    model_admin_class = type(get_model_name(model) + 'Admin', (admin.ModelAdmin,), kwargs)
    # print(model_admin_class)
    return model_admin_class


def auto_configure_admin_for_model(model, **kwargs):
    fields = get_fields_from_model(model)
    config = {}

    for admin_field in ADMIN_FIELDS:
        dev_value = kwargs.get(admin_field, None)
        if dev_value:
            config[admin_field] = dev_value
            continue

        strategy = STRATEGY.get(admin_field, None)
        if strategy:
            if callable(strategy):
                field_list = [field.name for field in fields if strategy(field)]
                # print(field_list)
                config[admin_field] = field_list
            else:
                config[admin_field] = strategy
        strategy = FINAL_STRATEGY.get(admin_field, None)
        if strategy and callable(strategy):
            config[admin_field] = strategy(config[admin_field])

    # get_many_to_many_fields_from_model(model)
    return create_admin_class(model, **config)


def auto_configure_admin_for_app(app):
    models = get_models_of_an_app(app)
    for model in models:
        admin_class = auto_configure_admin_for_model(model)
        register_admin_class(admin_class, override=False)


def auto_configure_admin(applications=[], exclude_applications=[]):
    apps = get_apps(applications, exclude_applications)
    for app in apps:
        auto_configure_admin_for_app(app)


def print_model_admin(admin_class):
    for field in ADMIN_FIELDS:
        value = admin_class.__dict__.get(field, None)
        if value:
            print('%s = %s' % (field, value))
