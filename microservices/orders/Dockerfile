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

http://192.168.10.10:8888/wp-json/wc/v3/orders

# Define environment variables
ENV MYSQL_DATABASE_USER=$MYSQL_DATABASE_USER
ENV MYSQL_DATABASE_PASSWORD=$MYSQL_DATABASE_PASSWORD
ENV MYSQL_DATABASE_DB=$MYSQL_DATABASE_DB
ENV MYSQL_DATABASE_HOST=$MYSQL_DATABASE_HOST
ENV API_URL=$API_URL
ENV CONSUMER_KEY=$CONSUMER_KEY
ENV CONSUMER_SECRET=$CONSUMER_SECRET
ENV SECRET_KEY=$SECRET_KEY
ENV NAME=$NAME

ENV NAME World

# Run the command to start the order.py script
CMD ["python", "order.py"]