FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY product.py /app
COPY requirements.txt /app
COPY secrets.env /app/secrets.env

# Create environment variables using Docker secrets


ENV MYSQL_DATABASE_USER_FILE=/run/secrets/mysql_database_user
ENV MYSQL_DATABASE_PASSWORD_FILE=/run/secrets/mysql_database_password
ENV MYSQL_DATABASE_DB_FILE=/run/secrets/mysql_database_db
ENV MYSQL_DATABASE_HOST_FILE=/run/secrets/mysql_database_host
ENV SECRET_KEY_FILE=/run/secrets/secret_key
ENV API_URL_FILE=/run/secrets/api_url
ENV CONSUMER_KEY_FILE=/run/secrets/consumer_key
ENV CONSUMER_SECRET_FILE=/run/secrets/consumer_secret

# Install any needed packages specified in requirements.txt

RUN pip install --trusted-host pypi.python.org -r requirements.txt


# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variables

ENV API_URL='http://192.168.10.10:8888/wp-json/wc/v3/products'
ENV CONSUMER_KEY='ck_c6534d9d3c818bfd23001cc3264f893d0f1e0145'
ENV CONSUMER_SECRET='cs_0746878dec7c520e920217c65397cb1241df75be'
ENV SECRET_KEY='sk_fYVw52zywDRVAgsC8yUi2TXFRu1MmtPK'

ENV NAME World

# Run the command to start the order.py script
CMD ["python", "product.py"]