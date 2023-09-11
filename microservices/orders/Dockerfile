# Use a minimal base image
FROM python:3.9-alpine AS base

# Add a non-root user to the image
RUN adduser -D phenix

# Set the working directory to /home/myuser/app
WORKDIR /home/myuser/app

# Copy the current directory contents into the container at /home/myuser/app
COPY order.py requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

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

# Use HEALTHCHECK instruction
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD curl --fail http://192.168.10.10:9090/ || exit 1

EXPOSE 9090

# Switch to the non-root user before running the container
USER phenix

# Run the command to start the order.py script
CMD ["python", "order.py"]
