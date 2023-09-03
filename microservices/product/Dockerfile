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

ENV API_URL='http://192.168.10.10/wp-json/wc/v3/products'
ENV CONSUMER_KEY='ck_1c8542dd8bb7b15edcde59f03607dd8375c21d11'
ENV CONSUMER_SECRET='cs_3da5306a5a407cc26d692e15c8ebf0db93f78421'
ENV SECRET_KEY='sk_fYVw52zywDRVAgsC8yUi2TXFRu1MmtPK'

ENV NAME World

# Run the command to start the order.py script
CMD ["python", "product.py"]