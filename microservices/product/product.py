from flask import Flask, jsonify, request, abort
from requests_oauthlib import OAuth1Session
import os

app = Flask(__name__)

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
api_url = os.getenv('API_URL')

@app.route('/add_product', methods=['POST'])
def add_product():
    # Get the product data from the request
    product_data = request.json

    # Check for empty fields
    required_fields = ['name', 'short_description', 'description', 'images']
    for field in required_fields:
        if field not in product_data or not product_data[field]:
            abort(400, f"Missing or empty field: {field}")

    # Validate regular_price
    if 'regular_price' not in product_data or not isinstance(product_data['regular_price'], (int, float)):
        abort(400, "regular_price must be a number")

    # Check for suspicious input
    suspicious_chars = ['<', '>', ';', "'", '"', '(', ')', '{', '}', '[', ']', '|', '&', '$', '#', '%', '@', '!', '`']
    for field in product_data:
        if isinstance(product_data[field], str) and any(char in product_data[field] for char in suspicious_chars):
            abort(400, "Input contains suspicious characters")

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

@app.route('/delete_product/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    # Set up the OAuth1Session for authentication
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)

    # Set up the API endpoint and headers
    headers = {'Content-Type': 'application/json'}

    # Send the DELETE request to delete the product
    try:
        response = oauth.delete(f'{api_url}/{product_id}', headers=headers)
        response.raise_for_status()
    except Exception as e:
        abort(400, str(e))

    # Handle the response from the WooCommerce API
    if response.status_code == 200:
        return jsonify({'message': 'Product deleted successfully.'}), 200
    else:
        abort(response.status_code, response.text)

@app.route('/update_product/<product_id>', methods=['PUT'])
def update_product(product_id):
    # Get the product data from the request
    product_data = request.json

    # Set up the OAuth1Session for authentication
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)

    # Set up the API endpoint and headers
    headers = {'Content-Type': 'application/json'}

    # Send the PUT request to update the product
    try:
        response = oauth.put(f'{api_url}/{product_id}', headers=headers, json=product_data)
        response.raise_for_status()
    except Exception as e:
        abort(400, str(e))

    # Handle the response from the WooCommerce API
    if response.status_code == 200:
        return jsonify({'message': 'Product updated successfully.'}), 200
    else:
        abort(response.status_code, response.text)
        
@app.route('/get_products', methods=['GET'])
def get_products():
    # Set up the OAuth1Session for authentication
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)

    # Set up the API endpoint and headers
    headers = {'Content-Type': 'application/json'}

    # Send the GET request to retrieve all products
    try:
        response = oauth.get(api_url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        abort(400, str(e))

    # Handle the response from the WooCommerce API
    if response.status_code == 200:
        products = response.json()
        return jsonify(products), 200
    else:
        abort(response.status_code, response.text)

@app.route('/get_product/<product_id>', methods=['GET'])
def get_product(product_id):
    # Set up the OAuth1Session for authentication
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)

    # Set up the API endpoint and  headers 
    headers = {'Content-Type': 'application/json'}
    
    # Send the GET request to retrieve the product
    try:
        response = oauth.get(f'{api_url}/{product_id}', headers=headers)
        response.raise_for_status()
    except Exception as e:
        abort(400, str(e))

    # Handle the response from the WooCommerce API
    if response.status_code == 200:
        product = response.json()
        return jsonify(product), 200
    else:
        abort(response.status_code, response.text)

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': str(error)}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found.'}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal server error.'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)