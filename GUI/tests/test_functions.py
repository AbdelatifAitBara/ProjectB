import unittest
# Now, import the 'microservice_gui' module from the 'app' directory
from app import microservice_gui

import requests
from flask.testing import FlaskClient
from app import create_app  # Import your Flask app factory function


class TestWebGui(unittest.TestCase):

    def test_is_empty(self):
        result = microservice_gui.is_empty('')       
        self.assertTrue(result)

        result = microservice_gui.is_empty(' ')       
        self.assertTrue(result)
    
        result = microservice_gui.is_empty('Hello, World!')
        self.assertFalse(result)

    # True if at the same time not empty, integer and positive
    def test_is_not_empty_integer(self):
        result = microservice_gui.is_not_empty_integer('5')
        self.assertTrue(result)

        result = microservice_gui.is_not_empty_integer('007')
        self.assertTrue(result)
        
        result = microservice_gui.is_not_empty_integer('0')
        self.assertFalse(result)

        result = microservice_gui.is_not_empty_integer('6U')
        self.assertFalse(result)

        result = microservice_gui.is_not_empty_integer('0.7')
        self.assertFalse(result)

        result = microservice_gui.is_not_empty_integer('-6')
        self.assertFalse(result)

        result = microservice_gui.is_not_empty_integer('')
        self.assertFalse(result)

        result = microservice_gui.is_not_empty_integer(' ')
        self.assertFalse(result)

        result = microservice_gui.is_not_empty_integer('Hello, World!')
        self.assertFalse(result)


    # True if at the same time not empty, float and positive
    def test_is_not_empty_float(self):
        result = microservice_gui.is_not_empty_float('5.5')
        self.assertTrue(result)

        result = microservice_gui.is_not_empty_float('5')
        self.assertTrue(result)

        result = microservice_gui.is_not_empty_float('007.7')
        self.assertTrue(result)
        
        result = microservice_gui.is_not_empty_float('0')
        self.assertFalse(result)

        result = microservice_gui.is_not_empty_float('6U')
        self.assertFalse(result)

        result = microservice_gui.is_not_empty_float('0.7')
        self.assertTrue(result)

        result = microservice_gui.is_not_empty_float('-6.5')
        self.assertFalse(result)

        result = microservice_gui.is_not_empty_float('')
        self.assertFalse(result)

        result = microservice_gui.is_not_empty_float(' ')
        self.assertFalse(result)

        result = microservice_gui.is_not_empty_float('Hello, World!')
        self.assertFalse(result)

''' 
    def setUp(self):
            app = create_app()
            self.client = app.test_client()

    def test_valid_input(self):
        response = self.client.post('/create-product', data={
            'name': '',
            'type': 'Product Type',
            'regular_price': '10.99',
            'description': 'Product Description',
            'short_description': 'Short Description',
            'image': 'product.jpg'
        })
        self.assertEqual(response.status_code, 200)
        # Add assertions for the response content, if needed 
        # Extract and decode the response content
        response_content = response.data.decode('utf-8')
    
    # Assert that the response content contains the expected message
        self.assertIn('Invalid input. Name field is empty.', response_content)
        #self.assertIn("Invalid input. Name field is empty.", response)  #Didnt work, because TypeError: argument of type 'WrapperTestResponse' is not iterable
        # This is code, which generate answer, and answer is too complex to be compaired
        # messages.append(f"{timestamp}: Request Sent: POST {url} Headers: {headers} Request body: {product_data}")
        # messages.append(f"{timestamp}: Response Received: {response.status_code} {response.text}")
        # return render_template("index.html", remaining_time=token_validity_duration, messages=messages)
'''
if __name__ == '__main__':
    unittest.main()
