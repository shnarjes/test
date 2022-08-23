from rest_framework.test import APIClient

from django.urls import reverse
from django.test import TestCase
from django.core.cache import cache

from product.models.products import Product
from product.models.category import Category
from product.models.color import Color


class ProductTest(TestCase):

    def setUp(self):
        color = Color.objects.create(title='red')
        category = Category.objects.create(title='digital')
        product = Product.objects.create(
            name='phone',
            price=9200000,
            capacity=5,
            cat=category,
            brand='man',
        )
        product.color.add(color)

    def test_cache_list_product(self):
        self.assertFalse(cache.get('product'))
        self.client.get(reverse('product:product-list'))
        self.assertTrue(cache.get('product'))

    def test_cache_retrieve_product(self):
        p = Product.objects.get(name='phone')
        pk = p.id
        key = "product" + str(pk)

        APIClient().get(reverse('product:product-detail', args=(p.id,)))
        self.assertTrue(cache.get(key))

    def test_cache_update(self):
        p = Product.objects.get(name='phone')
        pk = p.id
        key = "product" + str(pk)
        dict_product = {
            'name': 'phone2',
            'price': 1320000,
            'capacity': 5,
            'brand': 'man',
        }
        APIClient().put(reverse('product:product-detail', args=(p.id,)), dict_product)
        self.assertFalse(cache.get('product'))
        self.assertFalse(cache.get(key))

    def test_cache_delete(self):
        p = Product.objects.get(name='phone')
        pk = p.id
        key = "product" + str(pk)
        APIClient().delete(reverse('product:product-detail', args=(p.id,)))
        self.assertFalse(cache.get('product'))
        self.assertFalse(cache.get(key))
