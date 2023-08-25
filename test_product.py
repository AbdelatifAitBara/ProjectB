import unittest
import requests
import json


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://192.168.10.30:8080'
        self.consumer_key = 'ck_871224cf87f8459b0862453fa7e03dbe2accbecd'
        self.consumer_secret = 'cs_3f3dc3a74524e7f7442303a6e12ec03de5da505c'

    def test_add_product(self):
        # Define the product data to add
        product_data = {
            'name': 'Test Product',
            'type': 'simple',
            'regular_price': '10.00'
        }

        # Send the POST request to add the product
        response = requests.post(
            f'{self.base_url}/add_product',
            headers={'Content-Type': 'application/json'},
            json=product_data,
            auth=requests.auth.HTTPBasicAuth(self.consumer_key, self.consumer_secret)
        )

        # Check that the response is valid
        self.assertEqual(response.status_code, 201)
        self.assertIn('product_id', response.json())

    def test_delete_product(self):
        # Define the product ID to delete
        product_id = 1

        # Send the DELETE request to delete the product
        response = requests.delete(
            f'{self.base_url}/delete_product/{product_id}',
            headers={'Content-Type': 'application/json'},
            auth=requests.auth.HTTPBasicAuth(self.consumer_key, self.consumer_secret)
        )

        # Check that the response is valid
        self.assertIn(response.status_code, [200, 400])

    def test_update_product(self):
        # Define the product ID to update
        product_id = 1

        # Define the product data to update
        product_data = {
            'name': 'Updated Product',
            'regular_price': '15.00'
        }

        # Send the PUT request to update the product
        response = requests.put(
            f'{self.base_url}/update_product/{product_id}',
            headers={'Content-Type': 'application/json'},
            json=product_data,
            auth=requests.auth.HTTPBasicAuth(self.consumer_key, self.consumer_secret)
        )

        # Check that the response is valid
        self.assertIn(response.status_code, [200, 400])

    def test_add_product(self):
        # Define the product data to add
        product_data = {
            'name': 'Test Product',
            'type': 'simple',
            'regular_price': '10.00'
        }

        # Send the POST request to add the product
        response = requests.post(
            f'{self.base_url}/add_product',
            headers={'Content-Type': 'application/json'},
            json=product_data,
            auth=requests.auth.HTTPBasicAuth(self.consumer_key, self.consumer_secret)
        )

        # Print the response content for debugging
        print(response.content)

        # Check that the response is valid
        self.assertEqual(response.status_code, 201)
        self.assertIn('product_id', response.json())

if __name__ == '__main__':
    unittest.main()
