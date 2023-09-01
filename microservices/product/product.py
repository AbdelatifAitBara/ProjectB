from flask import Flask, abort, jsonify, request
from requests_oauthlib import OAuth1Session
import pymysql
from flask_cors import CORS
import json
import jwt
from functools import wraps
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app)

# Read the environment variables from the corresponding files


with open('/run/secrets/mysql_database_user', 'r') as f:
    app.config['MYSQL_DATABASE_USER'] = f.read().strip()

with open('/run/secrets/mysql_database_password', 'r') as f:
    app.config['MYSQL_DATABASE_PASSWORD'] = f.read().strip()

with open('/run/secrets/mysql_database_db', 'r') as f:
    app.config['MYSQL_DATABASE_DB'] = f.read().strip()

with open('/run/secrets/mysql_database_host', 'r') as f:
    app.config['MYSQL_DATABASE_HOST'] = f.read().strip()


API_URL = os.getenv('API_URL')
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')


@app.route('/token', methods=['POST'])
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
        return jsonify({'message': 'Authentication failed'}), 401
    
    # Set up the OAuth1Session for authentication
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)

    # Set up the API endpoint and headers
    headers = {'Content-Type': 'application/json'}

    # Send the POST request to add the product
    try:
        response = oauth.post(API_URL, headers=headers, json=product_data)
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
    except Exception as e:
        abort(400, str(e))

    # Handle the response from the WooCommerce API
    if response.status_code == 200:
        return jsonify({'message': 'Product deleted successfully.'}), 200
    else:
        abort(response.status_code, response.text)


@app.route('/update_product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    # Get the updated product data from the request
    product_data = request.json

    token = request.headers.get('Authorization')
    
    if not token_authorized(token):
        return jsonify({'message': 'Authentication failed'}), 401
    
    # Set up the OAuth1Session for authentication
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)

    # Set up the API endpoint and headers
    endpoint = f"{API_URL}/{product_id}"
    headers = {'Content-Type': 'application/json'}

    # Send the PUT request to update the product
    try:
        response = oauth.put(endpoint, headers=headers, json=product_data)
        response.raise_for_status()
    except Exception as e:
        abort(400, str(e))

    # Handle the response from the WooCommerce API
    if response.status_code == 200:
        return jsonify({'message': 'Product updated successfully.'}), 200
    else:
        abort(response.status_code, response.text)


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
    except Exception as e:
        abort(400, str(e))

    # Handle the response from the WooCommerce API
    if response.status_code == 200:
        product_data = response.json()
        return jsonify(product_data), 200
    else:
        abort(response.status_code, response.text)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
