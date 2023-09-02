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
        cur.execute("CREATE TABLE IF NOT EXISTS access_tokens_order (id INT(11) NOT NULL AUTO_INCREMENT, token VARCHAR(255) NOT NULL, PRIMARY KEY (id));")
        conn.commit()


@app.route('/order_token', methods=['POST'])
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
                    cur.execute("INSERT INTO access_tokens_order (token) VALUES (%s)", (token,))
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
                cur.execute("SELECT COUNT(*) FROM access_tokens_order WHERE token=%s", (token,))
                count = cur.fetchone()[0]
        if count > 0:
            return True
        else:
            return False
    except:
        return False

@app.route('/add_order', methods=['POST'])
def add_order():
    # Get the order data from the request
    order_data = request.json

    token = request.headers.get('Authorization')
    
    if not token_authorized(token):
        return jsonify({'message': 'Authentication failed'}), 401
    
    # Check if required fields are present and not empty
    required_fields = ['customer_name', 'customer_email']
    for field in required_fields:
        if field not in order_data or not order_data[field]:
            return jsonify({'message': f'{field} is a required field'}), 400
        
    # Set up the OAuth1Session for authentication
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)

    # Set up the API endpoint and headers
    headers = {'Content-Type': 'application/json'}

    # Send the POST request to add the order
    try:
        response = oauth.post(API_URL, headers=headers, json=order_data)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        error_message = e.response.json()['message']
        return jsonify({'message': f'Error adding order: {error_message}'}), e.response.status_code
    except Exception as e:
        return jsonify({'message': f'Error adding order: {str(e)}'}), 500

    # Handle the response from the WooCommerce API
    if response.status_code == 201:
        # Extract the order_id from the response body
        order_id = response.json()['id']
        return jsonify({'message': 'Order added successfully.', 'order_id': order_id}), 201
    else:
        return jsonify({'message': 'Error adding order.'}), 500


@app.route('/get_order/<int:order_id>', methods=['GET'])
def get_order(order_id):
    token = request.headers.get('Authorization')
    
    if not token_authorized(token):
        return jsonify({'message': 'Authentication failed'}), 401
    
    # Set up the OAuth1Session for authentication
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)

    # Set up the API endpoint and headers
    endpoint = f"{API_URL}/{order_id}"
    headers = {'Content-Type': 'application/json'}

    # Send the GET request to retrieve the order
    try:
        response = oauth.get(endpoint, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        error_message = e.response.json()['message']
        return jsonify({'message': f'Error getting order: {error_message}'}), e.response.status_code
    except Exception as e:
        return jsonify({'message': f'Error getting order: {str(e)}'}), 500

    # Handle the response from the WooCommerce API
    if response.status_code == 200:
        order_data = response.json()
        return jsonify(order_data), 200
    else:
        return jsonify({'message': 'Error getting order.'}), 500


@app.route('/update_order/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    # Get the updated order data from the request
    order_data = request.json

    token = request.headers.get('Authorization')
    
    if not token_authorized(token):
        return jsonify({'message': 'Authentication failed'}), 401
    
    # Set up the OAuth1Session for authentication
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)

    # Set up the API endpoint and headers
    endpoint = f"{API_URL}/{order_id}"
    headers = {'Content-Type': 'application/json'}

    # Send the PUT request to update the order
    try:
        response = oauth.put(endpoint, headers=headers, json=order_data)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        error_message = e.response.json()['message']
        return jsonify({'message': f'Error updating order: {error_message}'}), e.response.status_code
    except Exception as e:
        return jsonify({'message': f'Error updating order: {str(e)}'}), 500

    # Handle the response from the WooCommerce API
    if response.status_code == 200:
        return jsonify({'message': 'Order updated successfully.'}), 200
    else:
        return jsonify({'message': 'Error updating order.'}), 500


@app.route('/delete_order/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    token = request.headers.get('Authorization')
    
    if not token_authorized(token):
        return jsonify({'message': 'Authentication failed'}), 401
    
    # Set up the OAuth1Session for authentication
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)

    # Set up the API endpoint and headers
    endpoint = f"{API_URL}/{order_id}"
    headers = {'Content-Type': 'application/json'}

    # Send the DELETE request to delete the order
    try:
        response = oauth.delete(endpoint, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        error_message = e.response.json()['message']
        return jsonify({'message': f'Error deleting order: {error_message}'}), e.response.status_code
    except Exception as e:
        return jsonify({'message': f'Error deleting order: {str(e)}'}), 500

    # Handle the response from the WooCommerce API
    if response.status_code == 200:
        return jsonify({'message': 'Order deleted successfully.'}), 200
    else:
        return jsonify({'message': 'Error deleting order.'}), 500
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9090)