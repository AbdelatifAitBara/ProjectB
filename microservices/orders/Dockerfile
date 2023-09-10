FROM python:3.9-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY order.py requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variables
ENV MYSQL_DATABASE_USER=$MYSQL_DATABASE_USER \
    MYSQL_DATABASE_PASSWORD=$MYSQL_DATABASE_PASSWORD \
    MYSQL_DATABASE_DB=$MYSQL_DATABASE_DB \
    MYSQL_DATABASE_HOST=$MYSQL_DATABASE_HOST \
    API_URL=$API_URL \
    CONSUMER_KEY=$CONSUMER_KEY \
    CONSUMER_SECRET=$CONSUMER_SECRET \
    SECRET_KEY=$SECRET_KEY \
    NAME=$NAME

# Make port 9090 available to the world outside this container
EXPOSE 9090

# Use HEALTHCHECK instruction
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD curl --fail http://192.168.10.10:8080/ || exit 1


# Run the command to start the order.py script
CMD ["python", "order.py"]