from flask import Flask, abort, jsonify, request
import requests
from requests_oauthlib import OAuth1Session
import pymysql
from flask_cors import CORS
import json
import jwt
from functools import wraps
from datetime import datetime, timedelta
import os



app = Flask(__name__)

API_URL = os.getenv('API_URL')
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')

app.config['MYSQL_DATABASE_USER'] = 'phenix'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'wordpress_db'
app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


# Create a table to store the access tokens for the order if it doesn't exist

with pymysql.connect(
    host=app.config['MYSQL_DATABASE_HOST'],
    user=app.config['MYSQL_DATABASE_USER'],
    password=app.config['MYSQL_DATABASE_PASSWORD'],
    db=app.config['MYSQL_DATABASE_DB']
) as conn:
    with conn.cursor() as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS access_tokens_customer (id INT(11) NOT NULL AUTO_INCREMENT, token VARCHAR(255) NOT NULL, PRIMARY KEY (id));")
        conn.commit()

@app.route('/customer_token', methods=['POST'])
def customer_query():
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
                    cur.execute("INSERT INTO access_tokens_customer (token) VALUES (%s)", (token,))
                    conn.commit()
                    return jsonify({'access_token': token, 'token_type': 'bearer', 'expires_in': 120})
                else:
                    return jsonify({'message': 'Authentication failed'})
    except Exception as e:
        return str(e)

# Define a function to check if the customer token is authorized
def customer_token_authorized(token):
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
                cur.execute("SELECT COUNT(*) FROM access_tokens_customer WHERE token=%s", (token,))
                count = cur.fetchone()[0]
        if count > 0:
            return True
        else:
            return False
    except:
        return False


# Define a function to add a customer


@app.route('/add_customer', methods=['POST'])
def add_customer():
    customer_data = request.json

    token = request.headers.get('Authorization')

    if not customer_token_authorized(token):
        return jsonify({'message': 'Authentication failed'}), 401

    # Set up the OAuth1Session for authentication
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)

    # Set up the API endpoint and headers
    headers = {'Content-Type': 'application/json'}

    # Send the POST request to add the customer
    try:
        response = oauth.post(API_URL, headers=headers, json=customer_data)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        error_message = e.response.json()['message']
        return jsonify({'message': f'Error adding customer: {error_message}'}), e.response.status_code
    except Exception as e:
        return jsonify({'message': f'Error adding customer: {str(e)}'}), 500

    # Handle the response from the WooCommerce API
    if response.status_code == 201:
        # Extract the customer_id from the response body
        customer_id = response.json()['id']
        return jsonify({'message': 'Customer added successfully.', 'customer_id': customer_id}), 201
    else:
        return jsonify({'message': 'Error adding customer.'}), 500

# Define a function to delete a customer


@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    token = request.headers.get('Authorization')
    
    if not customer_token_authorized(token):
        return jsonify({'message': 'Authentication failed'}), 401
    
    # Set up the OAuth1Session for authentication
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)
    
    # Set up the API endpoint and headers
    headers = {'Content-Type': 'application/json'}
    
    # Send the DELETE request to remove the user
    try:
        response = oauth.delete(f"{API_URL}/{user_id}", headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        error_message = e.response.json()['message']
        return jsonify({'message': f'Error deleting user: {error_message}'}), e.response.status_code
    except Exception as e:
        return jsonify({'message': f'Error deleting user: {str(e)}'}), 500
    
    # Handle the response from the WooCommerce API
    if response.status_code == 200:
        return jsonify({'message': 'User deleted successfully.'}), 200
    else:
        return jsonify({'message': 'Error deleting user.'}), 500
    

# Define a function to update a customer

@app.route('/update_user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = request.json
    
    token = request.headers.get('Authorization')
    
    if not customer_token_authorized(token):
        return jsonify({'message': 'Authentication failed'}), 401
    
    # Set up the OAuth1Session for authentication
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)
    
    # Set up the API endpoint and headers
    headers = {'Content-Type': 'application/json'}
    
    # Send the PUT request to update the user
    try:
        response = oauth.put(f"{API_URL}/{user_id}", headers=headers, json=user_data)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        error_message = e.response.json()['message']
        return jsonify({'message': f'Error updating user: {error_message}'}), e.response.status_code
    except Exception as e:
        return jsonify({'message': f'Error updating user: {str(e)}'}), 500
    
    # Handle the response from the WooCommerce API
    if response.status_code == 200:
        return jsonify({'message': 'User updated successfully.'}), 200
    else:
        return jsonify({'message': 'Error updating user.'}), 500
    
# Define a function to get a customer

@app.route('/get_user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    token = request.headers.get('Authorization')
    
    if not customer_token_authorized(token):
        return jsonify({'message': 'Authentication failed'}), 401
    
    # Set up the OAuth1Session for authentication
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)
    
    # Set up the API endpoint and headers
    headers = {'Content-Type': 'application/json'}
    
    # Send the GET request to retrieve the user
    try:
        response = oauth.get(f"{API_URL}/{user_id}", headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        error_message = e.response.json()['message']
        return jsonify({'message': f'Error retrieving user: {error_message}'}), e.response.status_code
    except Exception as e:
        return jsonify({'message': f'Error retrieving user: {str(e)}'}), 500
    
    # Handle the response from the WooCommerce API
    if response.status_code == 200:
        user_data = response.json()
        return jsonify({'user': user_data}), 200
    else:
        return jsonify({'message': 'Error retrieving user.'}), 500
    
    
# Define a function to get all customers

@app.route('/get_users', methods=['GET'])
def get_users():
    token = request.headers.get('Authorization')
    
    if not customer_token_authorized(token):
        return jsonify({'message': 'Authentication failed'}), 401
    
    # Set up the OAuth1Session for authentication
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)
    
    # Set up the API endpoint and headers
    headers = {'Content-Type': 'application/json'}
    
    # Send the GET request to retrieve the users
    try:
        response = oauth.get(API_URL, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        error_message = e.response.json()['message']
        return jsonify({'message': f'Error retrieving users: {error_message}'}), e.response.status_code
    except Exception as e:
        return jsonify({'message': f'Error retrieving users: {str(e)}'}), 500
    
    # Handle the response from the WooCommerce API
    if response.status_code == 200:
        users_data = response.json()
        return jsonify({'users': users_data}), 200
    else:
        return jsonify({'message': 'Error retrieving users.'}), 500

    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7070)