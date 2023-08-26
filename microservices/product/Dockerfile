# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY product.py /app
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Define environment variables
ENV CONSUMER_KEY='ck_dee05a6912d2c948e9607abb9e6174b330e04e6b'
ENV CONSUMER_SECRET='cs_685e63b42008ef7ecb2ec9fc534b6b607fdee5ee'

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "product.py"]