from flask import Flask, jsonify, request
from requests_oauthlib import OAuth1Session
import os
import jwt
from datetime import datetime, timedelta
from functools import wraps
import pymysql
from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods.users import GetUserInfo






app = Flask(__name__)

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
api_url = os.getenv('API_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=1)




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
@app.route('/login', methods=['POST'])
def login():
    # Get the username and password from the request
    username = request.json['username']
    password = request.json['password']

    # Establish a connection to the MySQL database
        # Connect to the MySQL database
    cnx = pymysql.connect(user='root', password='password', host='db', database='wordpress_db', port=3306)
    cursor = cnx.cursor()

    # Execute the SELECT query to retrieve the user with the given username
    query = "SELECT user_pass FROM wp_users WHERE user_login = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    # Check if a user with the given username exists
    if result is None:
        return 'Invalid username', 401

    # Establish a connection to the WordPress XML-RPC API
    wp_client = Client('http://192.168.10.10:8080/xmlrpc.php', username, password)

    # Retrieve user information from the WordPress API
    user_info = wp_client.call(GetUserInfo())

    # Compare the password provided by the user with the password stored in the database
    if user_info.username == username:
        # Generate the access token
        access_token = jwt.encode({'username': username}, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'access_token': access_token}), 200
    else:
        return 'Invalid password', 401

    # Close the cursor and connection
    cursor.close()
    connection.close()


@app.route('/add_product', methods=['POST'])
@token_required
def add_product(current_user):
    # Check user role
    if users[current_user]['role'] != 'shop_manager':
        return jsonify({'error': 'Sorry, you are not authorized to access'}), 403

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