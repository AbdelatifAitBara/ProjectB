import unittest
import requests
import json

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.url = 'http://192.168.10.30:8080/add_product'
        self.headers = {'Content-Type': 'application/json'}
        self.product_data = {
            "name": "Test Product",
            "type": "simple",
            "regular_price": "10.00"
        }

    def test_add_product(self):
        response = requests.post(self.url, headers=self.headers, json=self.product_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('product_id', response.json())

if __name__ == '__main__':
    unittest.main()