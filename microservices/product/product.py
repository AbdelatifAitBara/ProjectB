from functools import wraps
from flask import Flask, request, jsonify
from requests_oauthlib import OAuth1Session
import pymysql
import os
from datetime import datetime, timedelta
import jwt


app = Flask(__name__)

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
api_url = os.getenv('API_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=1)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization

        if not auth or not check_credentials(auth.username, auth.password):
            return jsonify({'error': 'Could not verify your credentials.'}), 401

        return f(*args, **kwargs)

    return decorated

def check_credentials(username, password):
    # Connect to the MySQL database
    cnx = pymysql.connect(user='root', password='password', host='db', database='wordpress_db', port=3306)
    cursor = cnx.cursor()

    # Check if the username and password match in the database
    query = f"SELECT u.ID, u.user_login, u.user_email, m.meta_value FROM wp_users u JOIN wp_usermeta m ON u.ID = m.user_id WHERE m.meta_key = 'wp_capabilities' AND u.user_login = '{username}' AND m.meta_value = 'a:1:{{s:12:\"shop_manager\";b:1;}}'"
    cursor.execute(query)
    result = cursor.fetchone()

    # Close the database connection
    cursor.close()
    cnx.close()

    # Return True if the credentials are correct, otherwise False
    return result is not None

@app.route('/token', methods=['POST'])
def get_token():
    username = request.json.get('username')
    password = request.json.get('password')
    if check_credentials(username, password):
        secret_key = os.getenv('SECRET_KEY')
        expiration_time = datetime.utcnow() + timedelta(minutes=15)
        token = jwt.encode({'user': username, 'exp': expiration_time}, secret_key, algorithm="HS256")
        return jsonify({'access_token': token})
    else:
        return jsonify({'error': 'You are not authorized for this operation.'}), 401


@app.route('/add_product', methods=['POST'])
@token_required
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

    # Set up the OAuth1Session for authentication
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)

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
@token_required
def delete_product(current_user, product_id):
    # Check user role
    if users[current_user]['role'] != 'shop_manager':
        return jsonify({'error': 'Unauthorized access'}), 403

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
    # Check user role
    if users[current_user]['role'] != 'shop_manager':
        return jsonify({'error': 'Unauthorized access'}), 403

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
    # Check user role
    if users[current_user]['role'] != 'shop_manager':
        return jsonify({'error': 'Unauthorized access'}), 403

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
    app.run(debug=True, host='0.0.0.0', port=9090)