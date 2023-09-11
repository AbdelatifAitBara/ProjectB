FROM python:3.9-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY product.py requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Add firewall rule to only allow requests from 192.168.10.40
RUN apk add --no-cache iptables \
    && iptables -I INPUT -p tcp --dport 80 ! -s 192.168.10.40 -j DROP

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

# Run the command to start the product.py script
USER root
RUN apk add --no-cache iptables \
    && iptables -I INPUT -p tcp --dport 80 ! -s 192.168.10.40 -j DROP


# Run the command to start the product.py script
CMD ["python", "product.py"]
