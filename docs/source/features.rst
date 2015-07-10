.. _more:

Features and Configurations
*******************************************************************************

https://docs.djangoproject.com/en/dev/ref/contrib/admin/


Registering your models
===============================================================================

**Do not use** the standard Django method to register your application::

    from django.contrib import admin
    admin.site.register(YourModel, YourModelAdmin)

Rather that, register your models using one of the following functions, by *model* or *app* that it is explained in the following sections:

- **auto_configure_admin_for_model(model, override=False, **kwargs)**
- **auto_configure_admin_for_app(app, override=False)**
- **auto_configure_admin(applications=[], exclude_applications=[], override=False)**



Configuration per model
-------------------------------------------------------------------------------

Uset the ``auto_configure_admin_for_model`` method::

    from django_smart_autoregister import auto_configure_admin_for_model
    from django.contrib.auth.models import User

    auto_configure_admin_for_model(User)

To override the automatically generated config, you can set the ModelAdmin attribute as a ``auto_configure_admin_for_model`` method parameter::

    auto_configure_admin_for_model(User, raw_id_fields=[], search_fields=['email', 'username'])


Pay attention you can receive a AlreadyRegistered exception if you are trying to configure a model that has already been registered. If you want to override previous configurations, you can use like this::

    auto_configure_admin_for_model(User, raw_id_fields=[], search_fields=['email', 'username'], override=True)


Configure all models
-------------------------------------------------------------------------------

You can configure automatically all models of a list of applications defined in ``settings.INSTALLED_APPS``::

    # admin.py
    from django_smart_autoregister import auto_configure_admin
    auto_configure_admin(['your_app1', 'your_app2'])

    # or
    auto_configure_admin(applications=['your_app1', 'your_app2'])

Or you can automatically configure the admin for all apps defined in ``settings.INSTALLED_APPS``::

    from django_smart_autoregister import auto_configure_admin
    auto_configure_admin()

And to exclude some application::

    from django_smart_autoregister import auto_configure_admin
    auto_configure_admin(exclude_applications=['django.contrib.auth'])




Settings
===============================================================================


DSA_FIELD_STRATEGY
-------------------

Sometimes you can to override the default intelligence of the tool. To do that, define the **DSA_FIELD_STRATEGY** settings in your ``settings.py`` file::

    # Functions that receive a field instance (e.g: `models.CharField(max_length=1)`) and return a boolean
    # If this functions returns True, the field will be included in the admin attribute config (e.g: `Admin.raw_id_fields`)
    DSA_FIELD_STRATEGY = {
        'raw_id_fields': lambda field: True,
    }

**For example**, lets create a strategy that we will configure the `list_filter` for every model field that contains `choices`::

    # This module offers a set of useful introspection functions to manipulate Django models/fields
    from django_smart_autoregister.django_helper import field_has_choices

    class MyModel(models.Model):
        my_choices = models.CharField(max_length=2, choices=(('A', 'A'), ('B', 'B')))
        another_choices = models.CharField(max_length=2)

    DSA_FIELD_STRATEGY = {
        'list_filter': lambda field: field_has_choices(field),
    }

    # `Admin.list_filter` will return `['my_choices']`

Or we can customize some default values::

    DSA_FIELD_STRATEGY = {
        'list_per_page': 20,
        'list_max_show_all': 50,
    }


DSA_FULL_STRATEGY
-------------------

Sometimes you can put some intelligence after the value (e.g: `list_field = [field1, field2, field7]`) was created by the tool or by the **DSA_FIELD_STRATEGY** settings. To to that define a strategy that will receive the generated value and fixed it according to your ideas throw the settings **DSA_FULL_STRATEGY**::

    # function(values) => values
    DSA_FULL_STRATEGY = {
        'raw_id_fields': lambda values: values_updated,
    }

**For example**, we want to show in the maximum 5 columns in the admin list table::

    DSA_FULL_STRATEGY = {
        'list_display': lambda values: values[0:5],
    }

    # Without this config: Admin.list_display = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    # With this last config: Admin.list_display = ['a', 'b', 'c', 'd', 'e']
