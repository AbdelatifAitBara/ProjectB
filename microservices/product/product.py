from flask import Flask, jsonify, request
from requests_oauthlib import OAuth1Session
import os
import psycopg2
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
api_url = os.getenv('API_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=1)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

# Create a PostgreSQL client
conn = psycopg2.connect(app.config['SQLALCHEMY_DATABASE_URI'])
cur = conn.cursor()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]

        if not token:
            return jsonify({'error': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['user']
        except:
            return jsonify({'error': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

import psycopg2

@app.route('/token', methods=['POST'])
def get_token():
    username = request.json.get('username')
    password = request.json.get('password')

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host="192.168.10.30",
        port=5432,
        database="mydatabase",
        user="postgres",
        password="example"
    )

    # Execute a query to check if the username, password, and role are correct
    cur = conn.cursor()
    cur.execute("SELECT role FROM users WHERE username = %s AND password = %s AND role = %s", (username, password, "shop manager"))
    result = cur.fetchone()

    if result:
        secret_key = os.getenv('SECRET_KEY')
        expiration_time = datetime.utcnow() + timedelta(minutes=15)
        token = jwt.encode({'user': username, 'role': result[0], 'exp': expiration_time}, secret_key, algorithm="HS256")
        return jsonify({'access_token': token})
    else:
        return jsonify({'error': 'Invalid credentials or insufficient permissions'}), 401

@app.route('/add_product', methods=['POST'])
@token_required
def add_product(current_user):
    # Get the product data from the request
    product_data = request.json

    # Set up the OAuth1Session for authentication
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)

    # Set up the API endpoint and headers
    url = f'{api_url}/wp-json/wc/v3/products'
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {request.headers["Authorization"].split(" ")[1]}'}

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
@token_required
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
@token_required
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
@token_required
def get_product(current_user, product_id):
    # Set up the OAuth1Session for authentication
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)

    # Set up the API endpoint and  headers 
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
