from flask import Flask, jsonify, request
from requests_oauthlib import OAuth1Session

app = Flask(__name__)

@app.route('/add_product', methods=['POST'])
def add_product():
    # Get the product data from the request
    product_data = request.json

    # Set up the OAuth1Session for authentication
    consumer_key = 'ck_a5f11e0d2a04d974d877f6b8dfeb6f4f1a32b2e9'
    consumer_secret = 'cs_1e5b43eebc244d9a7917bec31cd181f25d6928a0'
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
    app.run(debug=True)