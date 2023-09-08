FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY product.py /app
COPY requirements.txt /app

# Install any other needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080


# Define environment variables
ENV MYSQL_DATABASE_USER='phenix'
ENV MYSQL_DATABASE_PASSWORD='password'
ENV MYSQL_DATABASE_DB='wordpress_db'
ENV MYSQL_DATABASE_HOST='db:3306'
ENV API_URL='http://192.168.10.10:8888/wp-json/wc/v3/products'
ENV CONSUMER_KEY='ck_390eac7097f5b4ef94ea63092b1f29573b301730'
ENV CONSUMER_SECRET='cs_5bd284f19d681f3f5a3fb19c81f67e79c3c59a1d'
ENV SECRET_KEY='sk_fYVw52zywDRVAgsC8yUi2TXFRu1MmtPK'
ENV NAME World

# Run the command to start the order.py script
CMD ["python", "product.py"]