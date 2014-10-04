from distutils.version import StrictVersion

import django

if StrictVersion(django.get_version()) >= StrictVersion('1.4'):
    from django.conf.urls import patterns, include, url
else:
    from django.conf.urls.defaults import patterns, include, url


from django.contrib import admin
# admin.autodiscover()

# from django_smart_autoregister import auto_configure_admin_for_model
# from django_smart_autoregister import auto_configure_admin
# from django.contrib.auth.models import User

# auto_configure_admin_for_model(User)

# or
# auto_configure_admin()

# or
# auto_configure_admin(exclude_applications=['django.contrib.auth'])

# or
# auto_configure_admin(applications=['your_app1', 'your_app2'])


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)
