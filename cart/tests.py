from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from categories.models import Category, Subcategory
from products.models import Product
from cart.models import CartItem


User = get_user_model()


class CartTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user',
                                             password='test_password',)
        category = Category.objects.create(name='Category', slug='category',
                                           image='category.png',)
        subcategory = Subcategory.objects.create(
            category=category, name='Subcategory',
            slug='subcategory', image='subcategory.png',
        )
        self.product = Product.objects.create(
            subcategory=subcategory, name='Product', slug='product',
            image_small='small.png', image_medium='medium.png',
            image_large='large.png', price='10.00',
        )

    def test_add_product_to_cart(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            '/api/cart/items/', {'product': self.product.id, 'quantity': 2,},
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CartItem.objects.get(user=self.user).quantity, 2,)

    def test_add_product_without_authentication(self):
        response = self.client.post(
            '/api/cart/items/', {'product': self.product.id, 'quantity': 1,},
        )
        self.assertEqual(response.status_code, 401)
