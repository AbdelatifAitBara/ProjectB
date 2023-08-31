from flask import Flask, request, jsonify
from requests_oauthlib import OAuth1Session
import os


app = Flask(__name__)

#consumer_key = os.getenv('CONSUMER_KEY')
#consumer_secret = os.getenv('CONSUMER_SECRET')
api_url = os.getenv('API_URL')

@app.route('/add_product', methods=['POST'])
def add_product():
    # Get the product data from the request
    product_data = request.json

    # Check if any field is empty
    for key, value in product_data.items():
        if not value:
            return jsonify({'error': f'{key} is required.'}), 400

    # Check if regular_price field contains only numbers and points
    if not all(char.isdigit() or char == '.' for char in product_data['regular_price']):
        return jsonify({'error': 'Regular price should only contain numbers and points.'}), 400

    # Get the customer_key and customer_secret from the request headers
    customer_key = request.headers.get('customer_key')
    customer_secret = request.headers.get('customer_secret')

    # Set up the OAuth1Session for authentication
    oauth = OAuth1Session(client_key=customer_key, client_secret=customer_secret)

    # Set up the API endpoint and headers
    url = f'{api_url}/wp-json/wc/v3/products'
    auth_header = request.headers.get('Authorization', '').split(' ')
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {auth_header[1]}'}

    # Send the POST request to add the product
    response = oauth.post(url, headers=headers, json=product_data)

    # Handle the response from the WooCommerce API
    if response.status_code == 201:
        # Extract the product_id from the response body
        product_id = response.json()['id']
        return jsonify({'message': 'Product added successfully.', 'product_id': product_id}), 201
    else:
        return jsonify({'error': 'Failed to add product.'}), 400




@app.route('/delete_product/<product_id>', methods=['DELETE'])
def delete_product(current_user, product_id):


    # Set up the OAuth1Session for authentication
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)

    # Set up the API endpoint and headers
    url = f'{api_url}/wp-json/wc/v3/products/{product_id}'
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {request.headers["Authorization"].split(" ")[1]}'}

    # Send the DELETE request to delete the product
    response = oauth.delete(url, headers=headers)

    # Handle the response from the WooCommerce API
    if response.status_code == 200:
        return jsonify({'message': 'Product deleted successfully.'}), 200
    else:
        return jsonify({'error': 'Failed to delete product.'}), 400

@app.route('/update_product/<product_id>', methods=['PUT'])
def update_product(current_user, product_id):

    # Get the product data from the request
    product_data = request.json

    # Set up the OAuth1Session for authentication
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)

    # Set up the API endpoint and headers
    url = f'{api_url}/wp-json/wc/v3/products/{product_id}'
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {request.headers["Authorization"].split(" ")[1]}'}

    # Send the PUT request to update the product
    response = oauth.put(url, headers=headers, json=product_data)

    # Handle the response from the WooCommerce API
    if response.status_code == 200:
        return jsonify({'message': 'Product updated successfully.'}), 200
    else:
        return jsonify({'error': 'Failed to update product.'}), 400

@app.route('/get_product/<product_id>', methods=['GET'])
def get_product(current_user, product_id):

    # Set up the OAuth1Session for authentication
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)

    # Set up the API endpoint and headers
    url = f'{api_url}/wp-json/wc/v3/products/{product_id}'
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {request.headers["Authorization"].split(" ")[1]}'}


    # Send the GET request to retrieve the product
    response = oauth.get(url, headers=headers)

    # Handle the response from the WooCommerce API
    if response.status_code == 200:
        product = response.json()
        return jsonify(product), 200
    else:
        return jsonify({'error': 'Failed to retrieve product.'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)