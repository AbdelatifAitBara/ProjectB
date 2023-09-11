# Use a minimal base image
FROM python:3.9-alpine AS base

# Add a non-root user to the image
RUN adduser -D phenix

# Set the working directory to /home/myuser/app
WORKDIR /home/myuser/app

# Copy the current directory contents into the container at /home/myuser/app
COPY product.py requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN apk add --no-cache iptables && \
    pip install --trusted-host pypi.python.org -r requirements.txt

# Use a multistage build
FROM base AS final

# Define environment variables with default values
ENV MYSQL_DATABASE_USER=default \
    MYSQL_DATABASE_PASSWORD=default \
    MYSQL_DATABASE_DB=default \
    MYSQL_DATABASE_HOST=default \
    API_URL=default \
    CONSUMER_KEY=default \
    CONSUMER_SECRET=default \
    SECRET_KEY=default \
    NAME=default

# Use a specific command for HEALTHCHECK
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD python -c 'import requests; res = requests.get("http://localhost:8080/"); res.raise_for_status()'

EXPOSE 8080

# Switch to the root user before running the iptables command
USER root

# Add iptables rule to restrict access to the container
RUN iptables -A INPUT -p tcp --dport 8080 -s 192.168.10.40 -j ACCEPT
RUN iptables -A INPUT -p tcp --dport 8080 -j DROP

# Switch back to the non-root user before running the product.py script
USER phenix

# Run the command to start the product.py script
CMD ["python", "product.py"]