# Use a minimal base image for the final stage
FROM ubuntu:latest AS final

# Set the working directory to /app
WORKDIR /app

# Update the package list and install necessary packages
RUN apt-get update && \
    apt-get install -y python3 python3-pip curl && \
    # Remove any temporary files and caches
    rm -rf /var/lib/apt/lists/*

# Copy only the necessary files for installation
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt && \
    # Remove any temporary files and caches
    rm -rf /root/.cache

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

# Use HEALTHCHECK instruction
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD curl --fail http://192.168.10.10:8080/ || exit 1

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Copy the product.py script to the container
COPY product.py ./

# Run the command to start the product.py script
CMD ["python3", "product.py"]