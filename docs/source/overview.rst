.. _overview:

Getting Started
*******************************************************************************

Basic Example of Usage
===============================================================================

In some ``admin.py`` file::

    from django_smart_autoregister import auto_configure_admin_for_model
    from django_smart_autoregister import auto_configure_admin
    from django.contrib.auth.models import User

    # ignore if User has already been registered
    auto_configure_admin_for_model(User)

    # replace User admin configuration if User model has already been registered
    auto_configure_admin_for_model(User, override=True)

    # or
    auto_configure_admin()

    # or
    auto_configure_admin(exclude_applications=['django.contrib.auth'])

    # or
    auto_configure_admin(applications=['your_app1', 'your_app2'])



Installation
===============================================================================

::

    pip install django-smart-autoregister

or::

    1. Download zip file
    2. Extract it
    3. Execute in the extracted directory: python setup.py install

Development version
-------------------------------------------------------------------------------

::

    pip install -e git+git@github.com:paulocheque/django-smart-autoregister.git#egg=django-smart-autoregister


requirements.txt
-------------------------------------------------------------------------------

::

    django-smart-autoregister==0.0.2
    # or use the development version
    git+git://github.com/paulocheque/django-smart-autoregister.git#egg=django-smart-autoregister


Upgrade
-------------------------------------------------------------------------------

::

    pip install django-smart-autoregister --upgrade --no-deps


Compatibility
===============================================================================

* Tested with Django 1.2, 1.3, 1.4, 1.5, 1.6, 1.7 and PyPy
* Tested with Python 2.7, 3.3 and 3.4


Motivation
===============================================================================

It is boring to configure Django admin application for every model. It is a replicated task most of the time. Just for some special customization or special behavior that we need to waste some time to do this.


External references
===============================================================================

  *
