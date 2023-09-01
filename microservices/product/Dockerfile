FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY product.py /app
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt

RUN pip install --trusted-host pypi.python.org -r requirements.txt


# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variables

ENV API_URL='http://192.168.10.10:8888/wp-json/wc/v3/products'
ENV CONSUMER_KEY='ck_c6534d9d3c818bfd23001cc3264f893d0f1e0145'
ENV CONSUMER_SECRET='cs_0746878dec7c520e920217c65397cb1241df75be'
ENV SECRET_KEY='sk_fYVw52zywDRVAgsC8yUi2TXFRu1MmtPK'
ENV DB_HOST = 'db'
ENV DB_USER = 'phenix'
ENV DB_PASSWORD = 'password'
ENV DB_NAME = 'wordpress_db'

ENV NAME World

# Run the command to start the order.py script
CMD ["python", "product.py"]