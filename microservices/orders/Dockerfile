FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY order.py /app
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt

RUN pip install --trusted-host pypi.python.org -r requirements.txt


# Make port 9090 available to the world outside this container
EXPOSE 9090

# Define environment variables

ENV API_URL='http://192.168.10.10:8888/wp-json/wc/v3/orders'
ENV CONSUMER_KEY='ck_0d42c10beec5423042ba88f3d0efea9036c91ecf'
ENV CONSUMER_SECRET='cs_dd7a195f73646422825b1c72713a7e023190ddb6'
ENV SECRET_KEY='sk_fYVw52zywDRVAgsC8yUi2TXFRu1MmtPK'

ENV NAME World

# Run the command to start the order.py script
CMD ["python", "order.py"]