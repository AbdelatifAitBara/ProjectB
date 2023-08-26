from flask import Flask, jsonify, request
from requests_oauthlib import OAuth1Session

app = Flask(__name__)

@app.route('/add_order', methods=['POST'])
def add_order():
    # Get the order data from the request
    order_data = request.json

    # Set up the OAuth1Session for authentication
    consumer_key = 'ck_dee05a6912d2c948e9607abb9e6174b330e04e6b'
    consumer_secret = 'cs_685e63b42008ef7ecb2ec9fc534b6b607fdee5ee'
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)

    # Set up the API endpoint and headers
    url = 'http://192.168.10.10:8080/wp-json/wc/v3/orders'
    headers = {'Content-Type': 'application/json'}

    # Send the POST request to add the order
    response = oauth.post(url, headers=headers, json=order_data)

    # Handle the response from the WooCommerce API
    if response.status_code == 201:
        order_id = response.json()['id']
        return jsonify({'message': 'Order added successfully.', 'order_id': order_id}), 201
    else:
        return jsonify({'error': 'Failed to add order.'}), 400

@app.route('/delete_order/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    # Set up the OAuth1Session for authentication
    consumer_key = 'ck_dee05a6912d2c948e9607abb9e6174b330e04e6b'
    consumer_secret = 'cs_685e63b42008ef7ecb2ec9fc534b6b607fdee5ee'
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)

    # Set up the API endpoint and headers
    url = f'http://192.168.10.10:8080/wp-json/wc/v3/orders/{order_id}'
    headers = {'Content-Type': 'application/json'}

    # Send the DELETE request to delete the order
    response = oauth.delete(url, headers=headers)

    # Handle the response from the WooCommerce API
    if response.status_code == 200:
        return jsonify({'message': 'Order deleted successfully.'}), 200
    else:
        return jsonify({'error': 'Failed to delete order.'}), 400

@app.route('/update_order/<order_id>', methods=['PUT'])
def update_order(order_id):
    # Get the order data from the request
    order_data = request.json

    # Set up the OAuth1Session for authentication
    consumer_key = 'ck_dee05a6912d2c948e9607abb9e6174b330e04e6b'
    consumer_secret = 'cs_685e63b42008ef7ecb2ec9fc534b6b607fdee5ee'
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)

    # Set up the API endpoint and headers
    url = f'http://192.168.10.10:8080/wp-json/wc/v3/orders/{order_id}'
    headers = {'Content-Type': 'application/json'}

    # Send the PUT request to update the order
    response = oauth.put(url, headers=headers, json=order_data)

    # Handle the response from the WooCommerce API
    if response.status_code == 200:
        return jsonify({'message': 'Order updated successfully.'}), 200
    else:
        return jsonify({'error': 'Failed to update order.'}), 400

@app.route('/get_order/<order_id>', methods=['GET'])
def get_order(order_id):
    # Set up the OAuth1Session for authentication
    consumer_key = 'ck_dee05a6912d2c948e9607abb9e6174b330e04e6b'
    consumer_secret = 'cs_685e63b42008ef7ecb2ec9fc534b6b607fdee5ee'
    oauth = OAuth1Session(client_key=consumer_key, client_secret=consumer_secret)

    # Set up the API endpoint and headers
    url = f'http://192.168.10.10:8080/wp-json/wc/v3/orders/{order_id}'
    headers = {'Content-Type': 'application/json'}

    # Send the GET request to retrieve the order
    response = oauth.get(url, headers=headers)

    # Handle the response from the WooCommerce API
    if response.status_code == 200:
        order = response.json()
        return jsonify(order), 200
    else:
        return jsonify({'error': 'Failed to retrieve order.'}), 400
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9090)