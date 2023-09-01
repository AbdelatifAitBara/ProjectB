import unittest
import json
from app import app

class TestAddProduct(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_add_product(self):
        # Define the product data
        product_data = {
            'name': 'Test Product',
            'regular_price': '10.99',
            'description': 'This is a test product',
            'short_description': 'Test product',
            'images': [
                {
                    'src': 'https://example.com/image.jpg'
                }
            ]
        }

        # Send a POST request to the /add_product endpoint with the product data
        response = self.app.post('/add_product', headers={'Authorization': 'Bearer test_token'}, json=product_data)

        # Verify that the response status code is 201
        self.assertEqual(response.status_code, 201)

        # Verify that the response contains the product_id
        response_data = json.loads(response.data)
        self.assertIn('product_id', response_data)

    def test_add_product_missing_fields(self):
        # Define the product data with missing fields
        product_data = {
            'name': 'Test Product',
            'regular_price': '10.99',
            'description': '',
            'short_description': '',
            'images': []
        }

        # Send a POST request to the /add_product endpoint with the product data
        response = self.app.post('/add_product', headers={'Authorization': 'Bearer test_token'}, json=product_data)

        # Verify that the response status code is 400
        self.assertEqual(response.status_code, 400)

        # Verify that the response contains the error message
        response_data = json.loads(response.data)
        self.assertIn('description is a required field', response_data['message'])
        self.assertIn('short_description is a required field', response_data['message'])
        self.assertIn('images is a required field', response_data['message'])

    def test_add_product_invalid_price(self):
        # Define the product data with an invalid price
        product_data = {
            'name': 'Test Product',
            'regular_price': 'invalid',
            'description': 'This is a test product',
            'short_description': 'Test product',
            'images': [
                {
                    'src': 'https://example.com/image.jpg'
                }
            ]
        }

        # Send a POST request to the /add_product endpoint with the product data
        response = self.app.post('/add_product', headers={'Authorization': 'Bearer test_token'}, json=product_data)

        # Verify that the response status code is 400
        self.assertEqual(response.status_code, 400)

        # Verify that the response contains the error message
        response_data = json.loads(response.data)
        self.assertIn('regular_price must be a valid integer or float', response_data['message'])

    def test_add_product_invalid_characters(self):
        # Define the product data with invalid characters
        product_data = {
            'name': 'Test Product',
            'regular_price': '10.99',
            'description': 'This is a test product with & invalid characters',
            'short_description': 'Test product',
            'images': [
                {
                    'src': 'https://example.com/image.jpg'
                }
            ]
        }

        # Send a POST request to the /add_product endpoint with the product data
        response = self.app.post('/add_product', headers={'Authorization': 'Bearer test_token'}, json=product_data)

        # Verify that the response status code is 400
        self.assertEqual(response.status_code, 400)

        # Verify that the response contains the error message
        response_data = json.loads(response.data)
        self.assertIn('description contains unacceptable characters', response_data['message'])

if __name__ == '__main__':
    unittest.main()