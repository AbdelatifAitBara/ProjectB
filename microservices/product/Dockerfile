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
ENV CONSUMER_KEY='ck_5ad581011f1b6108c8f4c682bdf395f40684c199'
ENV CONSUMER_SECRET='cs_48194148d627ca81c86591273cab03a99c9f4bb5'
ENV SECRET_KEY='sk_fYVw52zywDRVAgsC8yUi2TXFRu1MmtPK'

ENV NAME World

# Run the command to start the order.py script
CMD ["python", "product.py"]