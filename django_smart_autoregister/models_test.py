import six

import django
from django.db import models
from django.contrib.auth.models import User
from .django_helper import django_greater_than


class EmptyModel(models.Model):
    class Meta:
        app_label = 'django_smart_autoregister'

class SomeModel(models.Model):
    SAMPLE_CHOICES = (('1', 'One'), ('2', 'Two'), ('3', 'Three'))

    rel1 = models.ForeignKey(EmptyModel, related_name='rel1')
    rel2 = models.OneToOneField(EmptyModel, related_name='rel2')
    many2many = models.ManyToManyField(EmptyModel)

    small_string = models.CharField(max_length=10)
    string = models.CharField(max_length=150)
    long_string = models.CharField(max_length=200)
    text = models.TextField(max_length=255)
    with_choices = models.CharField(max_length=5, choices=SAMPLE_CHOICES, default='1')
    email = models.EmailField()
    ip = models.IPAddressField()
    slug = models.SlugField()
    url = models.URLField()

    integer = models.IntegerField()
    small_integer = models.SmallIntegerField()
    positive_small_integer = models.PositiveIntegerField()
    positive_small_integer = models.PositiveSmallIntegerField()
    big_integer = models.BigIntegerField()
    comma_integer = models.CommaSeparatedIntegerField(max_length=10)

    real = models.DecimalField(decimal_places=2, max_digits=15)
    float = models.FloatField()

    boolean = models.BooleanField(default=False)
    null_boolean = models.NullBooleanField(default=False)

    datetime = models.DateTimeField(auto_now=True, auto_now_add=True)
    date = models.DateField()
    time = models.TimeField()

    file = models.FileField(upload_to='/tmp')
    filepath = models.FilePathField()

    if django_greater_than('1.6'):
        binary = models.BinaryField()

    class Meta:
        app_label = 'django_smart_autoregister'


class NtoNModel(models.Model):
    rel1 = models.ForeignKey(EmptyModel, related_name='rell1')
    rel2 = models.ForeignKey(EmptyModel, related_name='rell2')
    small_string = models.CharField(max_length=10)

    class Meta:
        app_label = 'django_smart_autoregister'
