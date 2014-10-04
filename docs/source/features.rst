.. _more:

Configuration
*******************************************************************************

https://docs.djangoproject.com/en/dev/ref/contrib/admin/


Registering your models
===============================================================================

Do not use the standard Django method to register your application::

    from django.contrib import admin
    admin.site.register(YourModel, YourModelAdmin)

Rather that, register your models using the DSA methods, by *model* or *app* that it is explained in the following sections.


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

Sometimes you can to override the default intelligence of the tool. To do that, define the **DSA_FIELD_STRATEGY** settings in your ``settings.py`` file::

    # Functions that receive a field instance and return a boolean
    DSA_FIELD_STRATEGY = {
        'raw_id_fields': lambda field: True,
    }


Sometimes you can put some intelligence after the value was created by the tool or by the **DSA_FIELD_STRATEGY** settings. To to that define a strategy that will receive the generated value and fixed it according to your ideas throw the settings **DSA_FULL_STRATEGY**::

    # function(values) => values
    DSA_FULL_STRATEGY = {
        'raw_id_fields': lambda field: True,
    }
