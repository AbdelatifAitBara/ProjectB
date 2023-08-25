import unittest
from product import *

class TestProduct(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_get_product_success(self):
        # Test retrieving a product with a valid product ID
        response = self.app.get('/get_product/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('name', response.json)

    def test_get_product_invalid_id(self):
        # Test retrieving a product with an invalid product ID
        response = self.app.get('/get_product/invalid_id')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

    def test_get_product_invalid_auth(self):
        # Test retrieving a product with invalid authentication credentials
        response = self.app.get('/get_product/1', headers={'Authorization': 'invalid_token'})
        self.assertEqual(response.status_code, 401)

    def test_update_product_success(self):
        # Test updating a product with a valid product ID and valid data
        product_data = {
            "name": "Updated Product",
            "type": "simple",
            "regular_price": "20.00"
        }
        response = self.app.put('/update_product/1', json=product_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)

    def test_update_product_invalid_id(self):
        # Test updating a product with an invalid product ID and valid data
        product_data = {
            "name": "Updated Product",
            "type": "simple",
            "regular_price": "20.00"
        }
        response = self.app.put('/update_product/invalid_id', json=product_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

    def test_update_product_invalid_data(self):
        # Test updating a product with a valid product ID and invalid data
        product_data = {
            "name": "Updated Product",
            "type": "simple",
            "regular_price": "invalid_price"
        }
        response = self.app.put('/update_product/1', json=product_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

    def test_update_product_invalid_auth(self):
        # Test updating a product with invalid authentication credentials
        product_data = {
            "name": "Updated Product",
            "type": "simple",
            "regular_price": "20.00"
        }
        response = self.app.put('/update_product/1', json=product_data, headers={'Authorization': 'invalid_token'})
        self.assertEqual(response.status_code, 401)

    def test_delete_product_success(self):
        # Test deleting a product with a valid product ID
        response = self.app.delete('/delete_product/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)

    def test_delete_product_invalid_id(self):
        # Test deleting a product with an invalid product ID
        response = self.app.delete('/delete_product/invalid_id')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

    def test_delete_product_invalid_auth(self):
        # Test deleting a product with invalid authentication credentials
        response = self.app.delete('/delete_product/1', headers={'Authorization': 'invalid_token'})
        self.assertEqual(response.status_code, 401)
