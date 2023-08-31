from flask import Flask, jsonify, request, abort
from requests_oauthlib import OAuth1Session
import os

app = Flask(__name__)

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
api_url = os.getenv('API_URL')

# Function to validate the product data
def validate_product_data(product_data):
    if not product_data:
        abort(400, 'Product data is required.')

    # Check for empty fields
    if not all(product_data.values()):
        abort(400, 'Empty fields are not allowed.')

    # Check for special characters
    for key, value in product_data.items():
        if isinstance(value, str) and not value.isalnum() and key != 'regular_price':
            abort(400, f'Special characters are not allowed in {key}.')

    # Check for excessively long input
    max_length = 100  # Set the maximum length as per your requirement
    for key, value in product_data.items():
        if isinstance(value, str) and len(value) > max_length:
            abort(400, f'{key} exceeds the maximum length of {max_length} characters.')

    # Check for regular_price as number
    if 'regular_price' in product_data:
        try:
            float(product_data['regular_price'])
        except ValueError:
            abort(400, 'Regular price must be a number.')

@app.route('/add_product', methods=['POST'])
def add_product():
    # Get the product data from the request
    product_data = request.json

    # Validate the product data
    validate_product_data(product_data)

    # Set up the OAuth1Session for authentication
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)

    # Set up the API endpoint and headers
    headers = {'Content-Type': 'application/json'}

    # Send the POST request to add the product
    try:
        response = oauth.post(api_url, headers=headers, json=product_data)
        response.raise_for_status()
    except Exception as e:
        abort(400, str(e))

    # Handle the response from the WooCommerce API
    if response.status_code == 201:
        # Extract the product_id from the response body
        product_id = response.json()['id']
        return jsonify({'message': 'Product added successfully.', 'product_id': product_id}), 201
    else:
        abort(response.status_code, response.text)

# Other route functions...

# Error handlers...

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)