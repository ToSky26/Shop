from django.test import TestCase
from rest_framework.test import APIClient

from .models import Category, Subcategory


class CategoryAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(
            name='Овощи', slug='vegetables',
            image='categories/vegetables.jpg',
        )
        Subcategory.objects.create(
            category=self.category, name='Морковь', slug='carrots',
            image='subcategories/carrots.jpg',
        )

    def test_category_list_returns_nested_subcategories(self):
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        category = response.data['results'][0]
        self.assertEqual(category['name'], 'Овощи')
        self.assertEqual(len(category['subcategories']), 1)
        self.assertEqual(category['subcategories'][0]['name'], 'Морковь',)

    def test_category_list_is_paginated(self):
        response = self.client.get('/api/categories/?page_size=1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
