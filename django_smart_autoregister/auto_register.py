from django.conf import settings
from django.db.models import *

from .django_helper import *
from .django_admin_helper import *


def is_suitable_for_raw_id_fields(field):
    return is_relationship_field(field)

def is_suitable_for_list_display(field):
    return is_string(field) or is_boolean(field) or is_number(field) or is_datetime(field)

def is_suitable_for_list_display_links(field):
    return is_suitable_for_list_display(field)

def is_suitable_for_list_filter(field):
    return field_has_choices(field) or is_boolean(field)

def is_suitable_for_search_fields(field):
    return is_string(field)


# User settings or DSA default settings
try:
    DSA_LIST_PER_PAGE = int(settings.DSA_LIST_PER_PAGE) if hasattr(settings, 'DSA_LIST_PER_PAGE') else 5
    DSA_LIST_MAX_SHOW_ALL = int(settings.DSA_LIST_MAX_SHOW_ALL) if hasattr(settings, 'DSA_LIST_MAX_SHOW_ALL') else 50
    DSA_FIELD_STRATEGY = settings.DSA_FIELD_STRATEGY if hasattr(settings, 'DSA_FIELD_STRATEGY') else {}
    DSA_FULL_STRATEGY = settings.DSA_FULL_STRATEGY if hasattr(settings, 'DSA_FULL_STRATEGY') else {}
except Exception as e:
    raise Exception('DSA improperly configured. Please, check your settings.DSA_*: %s' % str(e))

# function(field) => boolean
FIELD_STRATEGY = {
    'raw_id_fields': is_suitable_for_raw_id_fields,
    'list_display': is_suitable_for_list_display,
    'list_display_links': is_suitable_for_list_display_links,
    'list_filter': is_suitable_for_list_filter,
    'search_fields': is_suitable_for_search_fields,
    'list_per_page': DSA_LIST_PER_PAGE,
    'list_max_show_all': DSA_LIST_MAX_SHOW_ALL,
}


def confirm_list_display(value):
    if not value:
        return ['id', '__str__']
    if len(value) < 2:
        new_value = ['id', '__str__']
        new_value.extend(value)
        return new_value
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

def get_strategy(dsa_default_settings, user_custom_settings):
    strategy = {}
    strategy.update(dsa_default_settings)
    strategy.update(user_custom_settings)
    return strategy

STRATEGY = get_strategy(FIELD_STRATEGY, DSA_FIELD_STRATEGY)
FINAL_STRATEGY = get_strategy(FULL_STRATEGY, DSA_FULL_STRATEGY)
# print(STRATEGY)
# print(FINAL_STRATEGY)


def add_fk_links(model, fields, admin_class):
    for field in fields:
        if is_relationship_field(field):
            try:
                method = staticmethod(lambda obj_id: get_admin_change_link(model, obj_id))
                setattr(admin_class, field.name + '_link', method)
            except Exception as e:
                print(str(e))


def auto_configure_admin_for_model(model, override=False, **kwargs):
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
    admin_class = create_admin_class(model, **config)
    add_fk_links(model, fields, admin_class)
    current_admin_class = register_admin_class(model, admin_class, override=override)
    return current_admin_class


def auto_configure_admin_for_app(app, override=False):
    models = get_models_of_an_app(app)
    for model in models:
        auto_configure_admin_for_model(model, override=override)


def auto_configure_admin(applications=[], exclude_applications=[], override=False):
    apps = get_apps(applications, exclude_applications)
    for app in apps:
        auto_configure_admin_for_app(app, override=override)
