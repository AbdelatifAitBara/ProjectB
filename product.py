import os
from flask import Flask, jsonify, request
from requests_oauthlib import OAuth1Session
import redis
import secrets
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file install python-dotenv - pip install python-dotenv

app = Flask(__name__)
redis_client = redis.Redis(host='localhost', port=6379, db=0)

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')

def validate_credentials(username, password):
    # Check if the credentials are stored in Redis
    stored_password = redis_client.get(username)
    if stored_password and stored_password.decode() == password:
        return True
    else:
        return False

def generate_access_token(username):
    # Generate an access token
    access_token = secrets.token_hex(16)

    # Store the access token in Redis with an expiration time
    redis_client.setex(access_token, 3600, username)

    return access_token

@app.route('/add_product', methods=['POST'])
def add_product():
    # Get the product data from the request
    product_data = request.json

    # Get the access token from the request headers
    access_token = request.headers.get('Authorization')

    # Check if the access token is valid
    username = redis_client.get(access_token)
    if not username:
        return jsonify({'error': 'Invalid access token.'}), 401

    # Set up the OAuth1Session for authentication
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)

    # Set up the API endpoint and headers
    url = 'http://192.168.10.10:8080/wp-json/wc/v3/products'
    headers = {'Content-Type': 'application/json'}

    # Send the POST request to add the product
    response = oauth.post(url, headers=headers, json=product_data)

    # Handle the response from the WooCommerce API
    if response.status_code == 201:
        return jsonify({'message': 'Product added successfully.'}), 201
    else:
        return jsonify({'error': 'Failed to add product.'}), 400

@app.route('/delete_product/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    # Get the access token from the request headers
    access_token = request.headers.get('Authorization')

    # Check if the access token is valid
    username = redis_client.get(access_token)
    if not username:
        return jsonify({'error': 'Invalid access token.'}), 401

    # Set up the OAuth1Session for authentication
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)

    # Set up the API endpoint and headers
    url = f'http://192.168.10.10:8080/wp-json/wc/v3/products/{product_id}'
    headers = {'Content-Type': 'application/json'}

    # Send the DELETE request to delete the product
    response = oauth.delete(url, headers=headers)

    # Handle the response from the WooCommerce API
    if response.status_code == 200:
        return jsonify({'message': 'Product deleted successfully.'}), 200
    else:
        return jsonify({'error': 'Failed to delete product.'}), 400

@app.route('/update_product/<product_id>', methods=['PUT'])
def update_product(product_id):
    # Get the product data from the request
    product_data = request.json

    # Get the access token from the request headers
    access_token = request.headers.get('Authorization')

    # Check if the access token is valid
    username = redis_client.get(access_token)
    if not username:
        return jsonify({'error': 'Invalid access token.'}), 401

    # Set up the OAuth1Session for authentication
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)

    # Set up the API endpoint and headers
    url = f'http://192.168.10.10:8080/wp-json/wc/v3/products/{product_id}'
    headers = {'Content-Type': 'application/json'}

    # Send the PUT request to update the product
    response = oauth.put(url, headers=headers, json=product_data)

    # Handle the response from the WooCommerce API
    if response.status_code == 200:
        return jsonify({'message': 'Product updated successfully.'}), 200
    else:
        return jsonify({'error': 'Failed to update product.'}), 400

@app.route('/get_product/<product_id>', methods=['GET'])
def get_product(product_id):
    # Get the access token from the request headers
    access_token = request.headers.get('Authorization')

    # Check if the access token is valid
    username = redis_client.get(access_token)
    if not username:
        return jsonify({'error': 'Invalid access token.'}), 401

    # Set up the OAuth1Session for authentication
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)

    # Set up the API endpoint and headers
    url = f'http://192.168.10.10:8080/wp-json/wc/v3/products/{product_id}'
    headers = {'Content-Type': 'application/json'}

    # Send the GET request to retrieve the product
    response = oauth.get(url, headers=headers)

    # Handle the response from the WooCommerce API
    if response.status_code == 200:
        product = response.json()
        return jsonify(product), 200
    else:
        return jsonify({'error': 'Failed to retrieve product.'}), 400

@app.route('/generate_token', methods=['POST'])
def generate_token():
    # Get the username and password from the request
    username = request.json.get('username')
    password = request.json.get('password')

    # Validate the credentials
    if not validate_credentials(username, password):
        return jsonify({'error': 'Invalid username or password.'}), 401

    # Generate and store the access token
    access_token = generate_access_token(username)

    return jsonify({'access_token': access_token}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)