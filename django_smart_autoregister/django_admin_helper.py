import six

from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.core.urlresolvers import reverse
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


def register_admin_class(model, admin_class, override=False):
    try:
        admin.site.register(model, admin_class)
        return admin_class
    except AlreadyRegistered:
        if override:
            admin.site.unregister(model)
            admin.site.register(model, admin_class)
            return admin_class
        else:
            return get_registered_admin(model)


def get_registered_admin(model):
    return admin.site._registry[model].__class__




def get_admin_change_link(model, obj_id):
    app_label = model._meta.app_label
    model_name = get_model_name(model)
    name = '%s(%s)' % (model_name, obj_id)
    reverse_url = 'admin:%s_%s_change' % (app_label.lower(), model_name.lower())
    # print(reverse_url)
    url = reverse(reverse_url, args=(obj_id,))
    try:
        from django.utils.html import format_html # Django >= 1.5
    except ImportError:
        from django.utils.safestring import mark_safe
        def conditional_escape(text):
            if isinstance(text, SafeData):
                return text
            else:
                return escape(text)

        def format_html(format_string, *args, **kwargs):
            args_safe = map(conditional_escape, args)
            kwargs_safe = dict([(k, conditional_escape(v)) for (k, v) in six.iteritems(kwargs)])
            return mark_safe(format_string.format(*args_safe, **kwargs_safe))
    return format_html('<a href="%s">%s</a>' % ( url, name ))


def print_model_admin(admin_class):
    for field in ADMIN_FIELDS:
        value = admin_class.__dict__.get(field, None)
        if value:
            print('%s = %s' % (field, value))
