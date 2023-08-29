# Use an official Python runtime as a parent image
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
ARG GIT_COMMIT
ENV CONSUMER_KEY='ck_dee05a6912d2c948e9607abb9e6174b330e04e6b'
ENV CONSUMER_SECRET='cs_685e63b42008ef7ecb2ec9fc534b6b607fdee5ee'
ENV API_URL='http://192.168.10.10:8080'

ENV USERNAME1=abdelatif \
    PASSWORD1=password \
    ROLE1=shop_manager \
    USERNAME2=user1 \
    PASSWORD2=password \
    ROLE2=regular_user

ENV NAME World

LABEL git_commit=$GIT_COMMIT

# Run the command to start the order.py script
CMD ["python", "order.py"]
