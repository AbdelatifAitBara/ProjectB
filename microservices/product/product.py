from flask import Flask, jsonify, request
from requests_oauthlib import OAuth1Session
import psycopg2
import os
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
api_url = os.getenv('API_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=1)

conn = psycopg2.connect(
    host="192.168.10.30",
    port="5432",
    database="mydatabase",
    user="postgres",
    password="example"
)

class Product:
    def __init__(self):
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                price NUMERIC(10, 2) NOT NULL
            )
        """)
        conn.commit()
        cursor.close()
        #conn.close()
        

    def add_product(self, current_user, product_data):
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

            # Insert the product data into the PostgreSQL database
            cursor = conn.cursor()
            cursor.execute("INSERT INTO prod (product_id, name, price) VALUES (%s, %s, %s)",
                        (product_id, product_data['name'], product_data['price']))
            conn.commit()

            return jsonify({'message': 'Product added successfully.', 'product_id': product_id}), 201
        else:
            return jsonify({'error': 'Failed to add product.'}), 400

    def delete_product(self, current_user, product_id):
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

    def update_product(self, current_user, product_id, product_data):
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

    def get_product(self, current_user, product_id):
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

product = Product()

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

@app.route('/token', methods=['POST'])
def get_token():
    username = request.json.get('username')
    password = request.json.get('password')
    
    if username == 'admin' and password == 'password':
        secret_key = os.getenv('SECRET_KEY')
        expiration_time = datetime.utcnow() + timedelta(minutes=15)
        token = jwt.encode({'user': username, 'exp': expiration_time}, secret_key, algorithm="HS256")
        return jsonify({'access_token': token})
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/add_product', methods=['POST'])
@token_required
def add_product(current_user):
    # Get the product data from the request
    product_data = request.json

    return product.add_product(current_user, product_data)

@app.route('/delete_product/<product_id>', methods=['DELETE'])
@token_required
def delete_product(current_user, product_id):
    return product.delete_product(current_user, product_id)

@app.route('/update_product/<product_id>', methods=['PUT'])
@token_required
def update_product(current_user, product_id):
    # Get the product data from the request
    product_data = request.json

    return product.update_product(current_user, product_id, product_data)

@app.route('/get_product/<product_id>', methods=['GET'])
@token_required
def get_product(current_user, product_id):
    return product.get_product(current_user, product_id)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)