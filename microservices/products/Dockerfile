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

# Run the command to start the order.py script
CMD ["sh", "-c", "python product.py $MYSQL_DATABASE_USER $MYSQL_DATABASE_PASSWORD $MYSQL_DATABASE_DB $API_URL $CONSUMER_KEY $CONSUMER_SECRET $SECRET_KEY $NAME"]

