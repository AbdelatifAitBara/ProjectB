import json, requests 
import unittest
from unittest.mock import patch, MagicMock
from app.microservice_gui import app  


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

#Test 1. Simple index availability   
    def test_index(self):
        # Test the index route
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Microservice: Product!', response.data)
        
#Test 2. Token request, Consumer_secret key field is empty        
    @patch('requests.post')  # Here is decorator listen to post request, which sends my app and respond to them
    def test_request_token_empty(self, mock_post):

        # Define the mock response data and status code
        mock_response_data = {'access-token': 'fake_access_token'}
        mock_status_code = 200

        # Create a MagicMock for the response
        mock_response = MagicMock()
        mock_response.status_code = mock_status_code
        mock_response.json.return_value = mock_response_data

        # Configure the mock post method to return the mock response
        mock_post.return_value = mock_response

        # Consumer_secret key field is empty.
        # MagicMock Emulate frontend html form: send POST request to /request-token (Flask app route)
        # At the same time MagicMock receive data from my flask backend app
        response = app.test_client().post('/product_token', data={'consumer_secret': ''})
        # Assertions
        self.assertEqual(response.status_code, mock_status_code)
        self.assertIn(b'Consumer_secret key field is empty.', response.data)  

#Test 3. Token request, all data correct
    @patch('requests.post')  # Here is decorator listen to post request, which sends my app and respond to them
    def test_request_token(self, mock_post):
       
        # Define the mock response data and status code
        mock_response_data = {'access_token': 'fake_access_token'}
        mock_status_code = 200

        # Create a MagicMock for the response
        mock_response = MagicMock()
        mock_response.status_code = mock_status_code
        mock_response.json.return_value = mock_response_data

        # Configure the mock post method to return the mock response
        mock_post.return_value = mock_response

        # Consumer_secret key field is NOT empty.
        # Emulate frontend html form: send POST request to /request-token (Flask app route)
        response = app.test_client().post('/product_token', data={'consumer_secret': 'any_consumer_secret'})
        # Assertions
        self.assertEqual(response.status_code, mock_status_code)
        self.assertIn(b'fake_access_token', response.data)  

#Test 4. Get Product, all data correct
    @patch('requests.post')  # Mock the response for the /request-token endpoint
    @patch('requests.get')   # Mock the response for the /get-product endpoint
    def test_get_product(self, mock_get, mock_post):
        # Mock the response for the /request-token endpoint
        mock_token_response_data = {'access_token': 'fake_access_token'}
        mock_token_status_code = 200

        mock_token_response = MagicMock()
        mock_token_response.status_code = mock_token_status_code
        mock_token_response.json.return_value = mock_token_response_data

        # Configure the mock post method to return the mock token response
        mock_post.return_value = mock_token_response

        app.test_client().post('/request-token', data={'consumer_secret': 'any_consumer_secret'})

        # Mock the response for the /get-product endpoint
        mock_product_response_data = {'name': 'Super Mario Bros.'}
        mock_product_status_code = 200

        mock_product_response = MagicMock()
        mock_product_response.status_code = mock_product_status_code
        mock_product_response.json.return_value = mock_product_response_data

        # Configure the mock get method to return the mock product response
        mock_get.return_value = mock_product_response

        url = f"/get-product"
        data = {'product_id': '23'} 
        
        response = app.test_client().post(url, data = data)  

        # Assertions
        self.assertEqual(response.status_code, mock_product_status_code)
        self.assertIn(b'Super Mario Bros.', response.data)


#Test 5. Get Product, product id is empty
    @patch('requests.post')  # Mock the response for the /request-token endpoint
    @patch('requests.get')   # Mock the response for the /get-product endpoint
    def test_get_product_empty_pr_id(self, mock_get, mock_post):
        # Mock the response for the /request-token endpoint
        mock_token_response_data = {'access_token': 'fake_access_token'}
        mock_token_status_code = 200

        mock_token_response = MagicMock()
        mock_token_response.status_code = mock_token_status_code
        mock_token_response.json.return_value = mock_token_response_data

        # Configure the mock post method to return the mock token response
        mock_post.return_value = mock_token_response

        app.test_client().post('/request-token', data={'consumer_secret': 'any_consumer_secret'})

        # Mock the response for the /get-product endpoint
        mock_product_response_data = {'name': 'Super Mario Bros.'}
        mock_product_status_code = 200

        mock_product_response = MagicMock()
        mock_product_response.status_code = mock_product_status_code
        mock_product_response.json.return_value = mock_product_response_data

        # Configure the mock get method to return the mock product response
        mock_get.return_value = mock_product_response

        url = f"/get-product"
        data = {'product_id': ''} 
        
        response = app.test_client().post(url, data = data)  

        # Assertions
        self.assertEqual(response.status_code, mock_product_status_code)
        self.assertIn(b'Invalid input. Please enter a valid integer', response.data)

#Test 6. Get Product, product id is not integer
    @patch('requests.post')  # Mock the response for the /request-token endpoint
    @patch('requests.get')   # Mock the response for the /get-product endpoint
    def test_get_product_pr_id_notint(self, mock_get, mock_post):
        # Mock the response for the /request-token endpoint
        mock_token_response_data = {'access_token': 'fake_access_token'}
        mock_token_status_code = 200

        mock_token_response = MagicMock()
        mock_token_response.status_code = mock_token_status_code
        mock_token_response.json.return_value = mock_token_response_data

        # Configure the mock post method to return the mock token response
        mock_post.return_value = mock_token_response

        app.test_client().post('/request-token', data={'consumer_secret': 'any_consumer_secret'})

        # Mock the response for the /get-product endpoint
        mock_product_response_data = {'name': 'Super Mario Bros.'}
        mock_product_status_code = 200

        mock_product_response = MagicMock()
        mock_product_response.status_code = mock_product_status_code
        mock_product_response.json.return_value = mock_product_response_data

        # Configure the mock get method to return the mock product response
        mock_get.return_value = mock_product_response

        url = f"/get-product"
        data = {'product_id': 'fdgsh'} 
        
        response = app.test_client().post(url, data = data)  

        # Assertions
        self.assertEqual(response.status_code, mock_product_status_code)
        self.assertIn(b'Invalid input. Please enter a valid integer', response.data)

#Test 7. Get Product, product id is not integer (float)
    @patch('requests.post')  # Mock the response for the /request-token endpoint
    @patch('requests.get')   # Mock the response for the /get-product endpoint
    def test_get_product_pr_id_float(self, mock_get, mock_post):
        # Mock the response for the /request-token endpoint
        mock_token_response_data = {'access_token': 'fake_access_token'}
        mock_token_status_code = 200

        mock_token_response = MagicMock()
        mock_token_response.status_code = mock_token_status_code
        mock_token_response.json.return_value = mock_token_response_data

        # Configure the mock post method to return the mock token response
        mock_post.return_value = mock_token_response

        app.test_client().post('/request-token', data={'consumer_secret': 'any_consumer_secret'})

        # Mock the response for the /get-product endpoint
        mock_product_response_data = {'name': 'Super Mario Bros.'}
        mock_product_status_code = 200

        mock_product_response = MagicMock()
        mock_product_response.status_code = mock_product_status_code
        mock_product_response.json.return_value = mock_product_response_data

        # Configure the mock get method to return the mock product response
        mock_get.return_value = mock_product_response

        url = f"/get-product"
        data = {'product_id': '12.08'} 
        
        response = app.test_client().post(url, data = data)  

        # Assertions
        self.assertEqual(response.status_code, mock_product_status_code)
        self.assertIn(b'Invalid input. Please enter a valid integer', response.data)

if __name__ == '__main__':
    unittest.main()
