from flask import Flask, jsonify, request
import requests
from requests_oauthlib import OAuth1Session
import pymysql
from flask_cors import CORS
import json
import jwt
from datetime import datetime, timedelta
import os
import re

app = Flask(__name__)
CORS(app)

app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_DATABASE_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_DATABASE_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.getenv('MYSQL_DATABASE_DB')
app.config['MYSQL_DATABASE_HOST'] = os.getenv('MYSQL_DATABASE_HOST')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

API_URL = os.getenv('API_URL')
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')

# Create a table to store the access tokens for the product if it doesn't exist

with pymysql.connect(
    host=app.config['MYSQL_DATABASE_HOST'],
    user=app.config['MYSQL_DATABASE_USER'],
    password=app.config['MYSQL_DATABASE_PASSWORD'],
    db=app.config['MYSQL_DATABASE_DB']
) as conn:
    with conn.cursor() as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS access_tokens_product (id INT(11) NOT NULL AUTO_INCREMENT, token VARCHAR(255) NOT NULL, PRIMARY KEY (id));")
        conn.commit()

@app.route('/product_token', methods=['POST'])
def query():
    try:
        data = json.loads(request.data)
        consumer_secret = data['consumer_secret']
        with pymysql.connect(
            host=app.config['MYSQL_DATABASE_HOST'],
            user=app.config['MYSQL_DATABASE_USER'],
            password=app.config['MYSQL_DATABASE_PASSWORD'],
            db=app.config['MYSQL_DATABASE_DB']
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM wp_woocommerce_api_keys WHERE consumer_secret=%s", (consumer_secret,))
                count = cur.fetchone()[0]
                if count > 0:
                    # Generate token
                    payload = {
                        'exp': datetime.utcnow() + timedelta(minutes=2),
                        'iat': datetime.utcnow(),
                        'sub': consumer_secret
                    }
                    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
                    # Save token to db
                    cur.execute("INSERT INTO access_tokens_product (token) VALUES (%s)", (token,))
                    conn.commit()
                    return jsonify({'access_token': token, 'token_type': 'bearer', 'expires_in': 120})
                else:
                    return jsonify({'message': 'Authentication failed'})
    except Exception as e:
        return str(e)

# Define a function to check if the token is authorized
def token_authorized(token):
    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        if datetime.utcnow() > datetime.fromtimestamp(decoded_token['exp']):
            return False
        with pymysql.connect(
            host=app.config['MYSQL_DATABASE_HOST'],
            user=app.config['MYSQL_DATABASE_USER'],
            password=app.config['MYSQL_DATABASE_PASSWORD'],
            db=app.config['MYSQL_DATABASE_DB']
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM access_tokens_product WHERE token=%s", (token,))
                count = cur.fetchone()[0]
        if count > 0:
            return True
        else:
            return False
    except:
        return False

@app.route('/add_product', methods=['POST'])
def add_product():
    # Get the product data from the request
    product_data = request.json

    token = request.headers.get('Authorization')
    
    if not token_authorized(token):
        return jsonify({'message': 'Authentication failed, your token has expired or is invalid'}), 401
    
    # Check if required fields are present and not empty
    required_fields = ['name', 'regular_price', 'description', 'short_description', 'images']
    for field in required_fields:
        if field not in product_data or not product_data[field]:
            return jsonify({'message': f'{field} is a required field'}), 400
    
    # Check if regular_price is a valid float or integer
    try:
        regular_price = float(product_data['regular_price'])
        if not isinstance(regular_price, (int, float)):
            raise ValueError
    except ValueError:
        return jsonify({'message': 'regular_price must be a valid integer or float'}), 400
    
    # Check for suspicious characters in input fields
    suspicious_chars = re.compile(r'[&,@,"\',`_,\\\]\[}{=<>\?!#~-]')
    for field in product_data:
        if isinstance(product_data[field], str) and suspicious_chars.search(product_data[field]):
            return jsonify({'message': f'{field} contains unacceptable characters'}), 400
        
    # Set up the OAuth1Session for authentication
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)

    # Set up the API endpoint and headers
    headers = {'Content-Type': 'application/json'}

    # Send the POST request to add the product
    try:
        response = oauth.post(API_URL, headers=headers, json=product_data)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        error_message = e.response.json()['message']
        return jsonify({'message': f'Error adding product: {error_message}'}), e.response.status_code
    except Exception as e:
        return jsonify({'message': f'Error adding product: {str(e)}'}), 500

    # Handle the response from the WooCommerce API
    if response.status_code == 201:
        # Extract the product_id from the response body
        product_id = response.json()['id']
        return jsonify({'message': 'Product added successfully.', 'product_id': product_id}), 201
    else:
        return jsonify({'message': 'Error adding product.'}), 500


@app.route('/get_product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    token = request.headers.get('Authorization')
    
    if not token_authorized(token):
        return jsonify({'message': 'Authentication failed'}), 401
    
    # Set up the OAuth1Session for authentication
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)

    # Set up the API endpoint and headers
    endpoint = f"{API_URL}/{product_id}"
    headers = {'Content-Type': 'application/json'}

    # Send the GET request to retrieve the product
    try:
        response = oauth.get(endpoint, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        error_message = e.response.json()['message']
        return jsonify({'message': f'Error getting product: {error_message}'}), e.response.status_code
    except Exception as e:
        return jsonify({'message': f'Error getting product: {str(e)}'}), 500

    # Handle the response from the WooCommerce API
    if response.status_code == 200:
        product_data = response.json()
        return jsonify(product_data), 200
    else:
        return jsonify({'message': 'Error getting product.'}), 500

@app.route('/update_product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    # Get the updated product data from the request
    product_data = request.json

    token = request.headers.get('Authorization')
    
    if not token_authorized(token):
        return jsonify({'message': 'Authentication failed'}), 401
    
    # Check if regular_price is a valid float or integer
    if 'regular_price' in product_data:
        try:
            regular_price = float(product_data['regular_price'])
            if not isinstance(regular_price, (int, float)):
                raise ValueError
        except ValueError:
            return jsonify({'message': 'regular_price must be a valid integer or float'}), 400
    
    # Set up the OAuth1Session for authentication
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)

    # Set up the API endpoint and headers
    endpoint = f"{API_URL}/{product_id}"
    headers = {'Content-Type': 'application/json'}

    # Send the PUT request to update the product
    try:
        response = oauth.put(endpoint, headers=headers, json=product_data)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        error_message = e.response.json()['message']
        return jsonify({'message': f'Error updating product: {error_message}'}), e.response.status_code
    except Exception as e:
        return jsonify({'message': f'Error updating product: {str(e)}'}), 500

    # Handle the response from the WooCommerce API
    if response.status_code == 200:
        return jsonify({'message': 'Product updated successfully.'}), 200
    else:
        return jsonify({'message': 'Error updating product.'}), 500

@app.route('/delete_product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    token = request.headers.get('Authorization')
    
    if not token_authorized(token):
        return jsonify({'message': 'Authentication failed'}), 401
    
    # Set up the OAuth1Session for authentication
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)

    # Set up the API endpoint and headers
    endpoint = f"{API_URL}/{product_id}"
    headers = {'Content-Type': 'application/json'}

    # Send the DELETE request to delete the product
    try:
        response = oauth.delete(endpoint, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        error_message = e.response.json()['message']
        return jsonify({'message': f'Error deleting product: {error_message}'}), e.response.status_code
    except Exception as e:
        return jsonify({'message': f'Error deleting product: {str(e)}'}), 500

    # Handle the response from the WooCommerce API
    if response.status_code == 200:
        return jsonify({'message': 'Product deleted successfully.'}), 200
    else:
        return jsonify({'message': 'Error deleting product.'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)