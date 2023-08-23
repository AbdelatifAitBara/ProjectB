from flask import Flask, jsonify, request
from requests_oauthlib import OAuth1Session

app = Flask(__name__)

@app.route('/add_product', methods=['POST'])
def add_product():
    # Get the product data from the request
    product_data = request.json

    # Set up the OAuth1Session for authentication
    consumer_key = 'ck_45af364bd5c238d072539bbc772751eae91fd01f'
    consumer_secret = 'cs_9216406678451e7ae9f3c2311d395ab86fd8b8ca'
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret) # We have http website that's why we use that type of authentication

    # Set up the API endpoint and headers
    url = 'http://192.168.10.10:8080/wp-json/wc/v3/products'
    headers = {'Content-Type': 'application/json'} # I had a big problem with this before find the solution

    # Send the POST request to add the product
    response = oauth.post(url, headers=headers, json=product_data)

    # Handle the response from the WooCommerce API
    if response.status_code == 201:
        return jsonify({'message': 'Product added successfully.'}), 201
    else:
        return jsonify({'error': 'Failed to add product.'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)