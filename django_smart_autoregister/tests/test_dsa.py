# coding: utf-8
import unittest

import six

import django
from django.test import TestCase
from django_dynamic_fixture import G, F, P

from django_smart_autoregister import *
from ..models import *


def assertContainsAll(list1, list2):
    """
    # True
    assertContainsAll([], [])
    assertContainsAll([1, 2, 3], [1, 2, 3])
    assertContainsAll([1, 2, 2, 3], [1, 2, 3])

    # False
    assertContainsAll([1, 2], [1, 2, 3])
    assertContainsAll([1, 2, 3], [])
    assertContainsAll([], [1, 2, 3])
    """
    total = len(set(list2))
    result = set(list2).intersection(set(list1))
    return (not list1 and not list2) or (total > 0 and len(result) == total)


class DSATests(TestCase):
    def setUp(self):
        self.admin_class = auto_configure_admin_for_model(SomeModel)

    def test_admin_model_information(self):
        print_model_admin(self.admin_class)
        # print(STRATEGY)
        # self.assertEquals(True, False) # For debug logs

    def test_model_is_valid(self):
        g = G(SomeModel)
        self.assertEquals(1, SomeModel.objects.count(), msg=P(g))

    def test_raw_id_fields(self):
        attrs = self.admin_class.__dict__['raw_id_fields']
        assertContainsAll(['rel1', 'rel2'], attrs)
        self.assertEquals(2, len(attrs))

    def test_list_display(self):
        attrs = self.admin_class.__dict__['list_display']
        cols = [
            'small_string',
            'string',
            'with_choices',
            'email',
            'ip',
            'slug',
            'url',
            'integer',
            'small_integer',
            'positive_small_integer',
            'positive_small_integer',
            'big_integer',
            'comma_integer',
            'real',
            'float',
            'boolean',
            'null_boolean',
            'datetime',
            'date',
            'time',
            'long_string',
            'text',
            'binary',
            'file',
            'filepath',
            'text',
        ]
        assertContainsAll(cols, attrs)

    def test_list_display_links(self):
        attrs = self.admin_class.__dict__['list_display_links']
        cols = [
            'id',
            '__str__',
            'small_string',
            'string',
            'with_choices',
            'email',
            'ip',
            'slug',
            'url',
            'integer',
            'small_integer',
            'positive_small_integer',
            'positive_small_integer',
            'big_integer',
            'comma_integer',
            'real',
            'float',
            'boolean',
            'null_boolean',
            'datetime',
            'date',
            'time',
            'long_string',
            'text',
        ]
        assertContainsAll(cols, attrs)

    def test_list_filter(self):
        attrs = self.admin_class.__dict__['list_filter']
        cols = [
            'with_choices',
            'boolean',
            'null_boolean',
        ]
        assertContainsAll(cols, attrs)
        self.assertEquals(3, len(attrs))

    def test_search_fields(self):
        attrs = self.admin_class.__dict__['search_fields']
        cols = [
            'small_string',
            'string',
            'email',
            'ip',
        ]
        assertContainsAll(cols, attrs)
        self.assertEquals(9, len(attrs))

    def test_general_configs(self):
        list_max_show_all = self.admin_class.__dict__['list_max_show_all']
        list_per_page = self.admin_class.__dict__['list_per_page']
        self.assertEquals(list_max_show_all, 50)
        self.assertEquals(list_per_page, 5)


class EmptyModelTests(TestCase):
    def setUp(self):
        self.admin_class = auto_configure_admin_for_model(EmptyModel)

    def test_admin_model_information(self):
        print_model_admin(self.admin_class)
        # print(STRATEGY)
        # self.assertEquals(True, False) # For debug logs

    def test_model_is_valid(self):
        g = G(EmptyModel)
        self.assertEquals(1, EmptyModel.objects.count(), msg=P(g))

    def test_raw_id_fields(self):
        attrs = self.admin_class.__dict__['raw_id_fields']
        self.assertEquals([], attrs)

    def test_list_display(self):
        attrs = self.admin_class.__dict__['list_display']
        self.assertEquals(['id', '__str__'], attrs)

    def test_list_display_links(self):
        attrs = self.admin_class.__dict__['list_display_links']
        self.assertEquals(['id', '__str__'], attrs)

    def test_list_filter(self):
        attrs = self.admin_class.__dict__['list_filter']
        self.assertEquals([], attrs)

    def test_search_fields(self):
        attrs = self.admin_class.__dict__['search_fields']
        self.assertEquals(['id'], attrs)

    def test_general_configs(self):
        list_max_show_all = self.admin_class.__dict__['list_max_show_all']
        list_per_page = self.admin_class.__dict__['list_per_page']
        self.assertEquals(list_max_show_all, 50)
        self.assertEquals(list_per_page, 5)


class NtoNModelTests(TestCase):
    def test_list_display_include_id_and_str(self):
        self.admin_class = auto_configure_admin_for_model(NtoNModel)

        attrs = self.admin_class.__dict__['list_display']
        self.assertEquals(['id', '__str__', 'small_string'], attrs)

        attrs = self.admin_class.__dict__['list_display_links']
        self.assertEquals(['id', '__str__', 'small_string'], attrs)


class AdditionalTests(TestCase):
    def test_dsa_do_not_override_user_configuration(self):
        admin_class = auto_configure_admin_for_model(EmptyModel, list_filter=['id'], list_display=['x'])
        attrs = admin_class.__dict__['list_filter']
        self.assertEquals(['id'], attrs)
        attrs = admin_class.__dict__['list_display']
        self.assertEquals(['x'], attrs)

    def test_it_is_possible_to_override_register(self):
        admin_class = auto_configure_admin_for_model(EmptyModel, list_filter=['id'], list_display=['x'])
        attrs = admin_class.__dict__['list_filter']
        self.assertEquals(['id'], attrs)

        admin_class = auto_configure_admin_for_model(EmptyModel, override=False)
        attrs = admin_class.__dict__['list_filter']
        self.assertEquals(['id'], attrs)

        admin_class = auto_configure_admin_for_model(EmptyModel, override=True)
        attrs = admin_class.__dict__['list_display']
        self.assertEquals(['id', '__str__'], attrs)

    def test_admin_class_contain_fk_links(self):
        admin_class = auto_configure_admin_for_model(NtoNModel)
        link_url1 = admin_class.rel1_link(1)
        link_url2 = admin_class.rel1_link(2)
        if django.VERSION >= (1, 10):
            self.assertEquals(link_url1, '<a href="/admin/django_smart_autoregister/ntonmodel/1/change/">NtoNModel(1)</a>')
            self.assertEquals(link_url2, '<a href="/admin/django_smart_autoregister/ntonmodel/2/change/">NtoNModel(2)</a>')
        else:
            self.assertEquals(link_url1, '<a href="/admin/django_smart_autoregister/ntonmodel/1/">NtoNModel(1)</a>')
            self.assertEquals(link_url2, '<a href="/admin/django_smart_autoregister/ntonmodel/2/">NtoNModel(2)</a>')
