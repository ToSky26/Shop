from rest_framework.test import APITestCase


class ProductTests(APITestCase):

    def test_get_products(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.data)
