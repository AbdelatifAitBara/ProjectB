# Use a minimal base image
FROM python:3.9-alpine AS base

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY product.py requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Add a non-root user to the image
RUN adduser -D myuser

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

# Switch to the non-root user before running the container
USER vagrant

# Run the command to start the product.py script
CMD ["python", "product.py"]
