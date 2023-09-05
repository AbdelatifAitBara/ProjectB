FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY customer.py /app
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt

RUN pip install --trusted-host pypi.python.org -r requirements.txt


# Make port 7070 available to the world outside this container
EXPOSE 7070

# Define environment variables

ENV API_URL='http://192.168.10.10:8888/wp-json/wc/v3/customers'
ENV CONSUMER_KEY='ck_e38653de8b25bd4178ddd577785b6840606f3267'
ENV CONSUMER_SECRET='cs_f14c2e3e63c8c7826cddf552ea99ae6427405f9e'
ENV SECRET_KEY='sk_fYVw52zywDRVAgsC8yUi2TXFRu1MmtPK'

ENV NAME World

# Run the command to start the order.py script
CMD ["python", "customer.py"]