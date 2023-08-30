from flask import Flask, jsonify, request
from requests_oauthlib import OAuth1Session
import os
import jwt
from datetime import datetime, timedelta
from functools import wraps
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import mysql.connector


app = Flask(__name__)

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
api_url = os.getenv('API_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=1)


db_connection = mysql.connector.connect(
    host='192.168.10.10',
    user='phenix',
    password='password',
    database='wordpress_db'
)

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

@csrf_exempt
def get_token(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = User.objects.filter(username=username).first()

        if user is not None and user.check_password(password) and role == "shop_manager":
            secret_key = os.getenv('SECRET_KEY')
            expiration_time = datetime.utcnow() + timedelta(minutes=15)
            token = jwt.encode({'user': username, 'exp': expiration_time}, secret_key, algorithm="HS256")

            cursor = db_connection.cursor()
            cursor.execute("INSERT INTO tokens (access_token) VALUES (%s)", (token,))
            db_connection.commit()

            return JsonResponse({'access_token': token})
        elif user is not None and user.check_password(password) and role != "shop_manager":
            return JsonResponse({'error': 'Not authorized'}, status=401)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

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
    app.run(debug=True, host='0.0.0.0', port=8080)