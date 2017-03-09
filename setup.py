#from distutils.core import setup
from setuptools import setup, find_packages

# http://guide.python-distribute.org/quickstart.html
# python setup.py sdist
# python setup.py register
# python setup.py sdist upload
# pip install django-dynamic-fixture
# pip install django-dynamic-fixture --upgrade --no-deps
# Manual upload to PypI
# http://pypi.python.org/pypi/django-smart-autoregister
# Go to 'edit' link
# Update version and save
# Go to 'files' link and upload the file

VERSION = '0.0.5'

tests_require = [
    'nose==1.3.7',
    'django-nose==1.4.4',
    'coverage==3.7.1',
    'django-coverage==1.2.4',
    'tox==2.6.0',
    'flake8==2.1.0',
    'pyflakes==1.5.0',
    'pylint==1.6.5',
    'jsonfield==2.0.0',
    'django_dynamic_fixture==1.9.3',
]

install_requires = [
    'six==1.10.0',
    # 'django',
]

setup(name='django-smart-autoregister',
      url='https://github.com/paulocheque/django-smart-autoregister',
      author="paulocheque",
      author_email='paulocheque@gmail.com',
      keywords='python django admin autoregister',
      description='Automatically register models in the admin interface in a smart way.',
      license='MIT',
      classifiers=[
          'Framework :: Django',
          'Operating System :: OS Independent',
          'Topic :: Software Development',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: Implementation :: PyPy',
      ],

      version=VERSION,
      install_requires=install_requires,
      tests_require=tests_require,
      test_suite='runtests.runtests',
      extras_require={'test': tests_require},

      entry_points={ 'nose.plugins': [] },
      packages=find_packages(),
)
