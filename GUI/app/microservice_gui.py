from flask import Flask, render_template, request
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

messages = []  # Create a list to store messages

token_validity_duration = 120  # Define the token validity duration in seconds
token_valid_until = None  # Initialize token validity time
access_token = None  # Initialize access_token

##Below are validation function, just to keep code readable and suitable for testing
# Validation function for checking if a value is empty (blank or whitespace-only)
def is_empty(value):
    return not value.strip()  # Strip removes leading and trailing whitespace

# Validation function for checking if a value is not empty and an integer > 0
def is_not_empty_integer(value):
    try:
        int_value = int(value)
        return value.strip() and int_value > 0
    except ValueError:
        return False

# Validation function for checking if a value is not empty and a float > 0
def is_not_empty_float(value):
    value = value.strip()
    try:
        float(value)
        return float(value) > 0  # Value is a valid float > 0
    except ValueError:
        return False  # Value is not a valid float

#Complex validation functions
def validate_product_form(name, type, regular_price, description, short_description, image):
    errors = []

    if is_empty(name):
        messages.append("Invalid input. Name field is empty.")
        return render_template("index.html", remaining_time=token_validity_duration, messages=messages)
       
    if is_empty(type):
        messages.append("Invalid input. Type field is empty.")
        return render_template("index.html", remaining_time=token_validity_duration, messages=messages)

    if not is_not_empty_float(regular_price):
        messages.append("Invalid input. Please enter a valid float > 0 into Regulare price field.")
        return render_template("index.html", remaining_time=token_validity_duration, messages=messages)
    
    if is_empty(description):
        messages.append("Invalid input. Description field is empty.")
        return render_template("index.html", remaining_time=token_validity_duration, messages=messages)
    
    if is_empty(short_description):
        messages.append("Invalid input. Short description field is empty.")
        return render_template("index.html", remaining_time=token_validity_duration, messages=messages)
    
    if is_empty(image):
        messages.append("Invalid input. Image field is empty.")
        return render_template("index.html", remaining_time=token_validity_duration, messages=messages)

def validate_update_form(product_id, attribute, value):
    errors = []

    if not is_not_empty_float(product_id):
        messages.append("Invalid input. Please enter a valid Product ID.")
        return render_template("index.html", remaining_time=token_validity_duration, messages=messages)
    
    if is_empty(attribute):
        messages.append("Invalid input. Attribute field is empty.")
        return render_template("index.html", remaining_time=token_validity_duration, messages=messages)
       
    if is_empty(value):
        messages.append("Invalid input. Value field is empty.")
        return render_template("index.html", remaining_time=token_validity_duration, messages=messages)


##Here start endpoints codes
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/product_token", methods=["POST"])
def request_token():
    global access_token
    global token_valid_until
    current_time = datetime.now()
    token_valid_until = current_time + timedelta(seconds=token_validity_duration)

    if request.method == "POST":
        consumer_secret = request.form.get("consumer_secret")
        
        if is_empty(consumer_secret):
            messages.append("Consumer_secret key field is empty.")
            return render_template("index.html", remaining_time=token_validity_duration, messages=messages)
        else:
        # Continue with the valid input and request to the microservice

            # Capture the current timestamp
            timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

            # Send a POST request to the microservice
            url = "http://192.168.10.10:8080/product_token"
            data = {"consumer_secret": consumer_secret}

            try:
                response = requests.post(url, json=data)
                response_data = response.json()

                # Store the sent and received messages
                messages.append(f"{timestamp}: Request Sent: {request.method} {url} Body: {data}")
                messages.append(f"{timestamp}: Response Received: {response.status_code} {response.json()}")

                # Store the received access token
                access_token = response_data.get("access_token")

            except Exception as e:
                error_message = str(e)

        return render_template("index.html", remaining_time=token_validity_duration, messages=messages, token_valid_until=token_valid_until, now=current_time)


@app.route("/get-product", methods=["POST"])
def get_product():
    # Access the global token_valid_until, token_validity_duration and access_token variables
    global token_valid_until
    global token_validity_duration
    global access_token

    product_id = request.form.get("product_id")

    # Capture the current timestamp
    current_time = datetime.now()
    timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
    token_valid_until = current_time + timedelta(seconds=token_validity_duration)

    if not is_not_empty_integer(product_id):
        messages.append("Invalid input. Please enter a valid integer > 0.")
        return render_template("index.html", remaining_time=token_validity_duration, messages=messages)
    else:
        # Continue with the valid input and request to the microservice
        # Check if the access token is valid
        if current_time < token_valid_until:
            try:
                # Send a GET request to the microservice
                url = f"http://192.168.10.10:8080/get_product/{product_id}"
                headers = {"Authorization": f"{access_token}"}
                response = requests.get(url, headers=headers)
                #response_data = response.json()
                # Store the sent and received messages
                messages.append(f"{timestamp}: Request Sent: GET {url} Headers: {headers}")
                messages.append(f"{timestamp}: Response Received: {response.status_code} {response.json()}")
                return render_template("index.html", remaining_time=token_validity_duration, messages=messages)
            
            except Exception as e:
                error_message = str(e)
                messages.append(f"{timestamp}: Error: {error_message}")
                return render_template("index.html", remaining_time=token_validity_duration, messages=messages)
        else:
            messages.append("Access token is not valid. Please request a new token.")
            return render_template("index.html", remaining_time=token_validity_duration, messages=messages)


@app.route("/delete-product", methods=["POST"])
def delete_product():
    # Access the global token_valid_until, token_validity_duration and access_token variables
    global token_valid_until
    global token_validity_duration
    global access_token

    product_id = request.form.get("product_id")

    # Capture the current timestamp
    current_time = datetime.now()
    timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
    token_valid_until = current_time + timedelta(seconds=token_validity_duration)

    if not is_not_empty_integer(product_id):
        messages.append("Invalid input. Please enter a valid integer > 0.")
        return render_template("index.html", remaining_time=token_validity_duration, messages=messages)
    else:
        # Continue with the valid input and request to the microservice
        # Check if the access token is valid
        if current_time < token_valid_until:
            try:
                # Send a DELETE request to the microservice
                url = f"http://192.168.10.10:8080/delete_product/{product_id}?force=true"
                headers = {"Authorization": f"{access_token}"}
                response = requests.delete(url, headers=headers)

                # Store the sent and received messages
                messages.append(f"{timestamp}: Request Sent: DELETE {url} Headers: {headers}")
                messages.append(f"{timestamp}: Response Received: {response.status_code} {response.text}")

                return render_template("index.html", remaining_time=token_validity_duration, messages=messages)
            except Exception as e:
                error_message = str(e)
                messages.append(f"{timestamp}: Error: {error_message}")
        else:
            messages.append("Access token is not valid. Please request a new token.")
            return render_template("index.html", remaining_time=token_validity_duration, messages=messages)


@app.route("/create-product", methods=["POST"])
def create_product():
    # Access the global token_valid_until, token_validity_duration and access_token variables
    global token_valid_until
    global token_validity_duration
    global access_token

    name = request.form.get('name')
    type = request.form.get('type')
    regular_price = request.form.get('regular_price')
    description = request.form.get('description')
    short_description = request.form.get('short_description')
    image = request.form.get('image')

    # Create product data
    product_data = {
        "name": name,
        "type": type,
        "regular_price": regular_price,
        "description": description,
        "short_description": short_description,
        "images": [
            {
                "src": image
            }
        ]
    }

    # Capture the current timestamp
    current_time = datetime.now()
    timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
    token_valid_until = current_time + timedelta(seconds=token_validity_duration)

    validation_errors = validate_product_form(name, type, regular_price, description, short_description, image)

    if validation_errors:
        messages.append("Invalid input. Please enter a valid information.")
        return render_template("index.html", remaining_time=token_validity_duration, messages=messages)
    else:
        # Continue with the valid input and request to the microservice
        # Check if the access token is valid
        if current_time < token_valid_until:
            try:
                # Send a DELETE request to the microservice
                url = f"http://192.168.10.10:8080/add_product"
                headers = {"Authorization": f"{access_token}"}
                response = requests.post(url, headers=headers, json=product_data)

                # Store the sent and received messages
                messages.append(f"{timestamp}: Request Sent: POST {url} Headers: {headers} Request body: {product_data}")
                messages.append(f"{timestamp}: Response Received: {response.status_code} {response.text}")
                return render_template("index.html", remaining_time=token_validity_duration, messages=messages)
            except Exception as e:
                error_message = str(e)
                messages.append(f"{timestamp}: Error: {error_message}")
        else:
            messages.append("Access token is not valid. Please request a new token.")
            return render_template("index.html", remaining_time=token_validity_duration, messages=messages)

@app.route("/update-product", methods=["POST"])
def update_product():
    # Access the global token_valid_until, token_validity_duration and access_token variables
    global token_valid_until
    global token_validity_duration
    global access_token

    product_id = request.form.get('product_id')
    attribute = request.form.get('attribute')
    value = request.form.get('value')

    # Create product data
    product_data = {
        "product_id": product_id,
        "attribute": attribute,
        "value": value,
    }

    # Capture the current timestamp
    current_time = datetime.now()
    timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
    token_valid_until = current_time + timedelta(seconds=token_validity_duration)

    validation_errors = validate_update_form(product_id, attribute, value)

    if validation_errors:
        messages.append("Invalid input. Please enter a valid information.")
        return render_template("index.html", remaining_time=token_validity_duration, messages=messages)
    else:
        # Continue with the valid input and request to the microservice
        # Check if the access token is valid
        if current_time < token_valid_until:
            try:
                # Send a Update request to the microservice
                url = f"http://192.168.10.10:8080/update_product/{product_id}"
                headers = {"Authorization": f"{access_token}"}
                response = requests.put(url, headers=headers, json=product_data)

                # Store the sent and received messages
                messages.append(f"{timestamp}: Request Sent: PUT {url} Headers: {headers} Request body: {product_data}")
                messages.append(f"{timestamp}: Response Received: {response.status_code} {response.text}")
                return render_template("index.html", remaining_time=token_validity_duration, messages=messages)
            except Exception as e:
                error_message = str(e)
                messages.append(f"{timestamp}: Error: {error_message}")
        else:
            messages.append("Access token is not valid. Please request a new token.")
            return render_template("index.html", remaining_time=token_validity_duration, messages=messages)

if __name__ == "__main__":
    app.run(debug=True)
