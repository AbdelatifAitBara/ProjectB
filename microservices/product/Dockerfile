# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY product.py /app
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt


# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variables
ARG GIT_COMMIT
ENV CONSUMER_KEY='ck_5ea6e1894b318ed93e028f1cb3bb9dd1be1a6867'
ENV CONSUMER_SECRET='cs_a964eb3fe4271c76eb033da2bec40381405d516b'
ENV API_URL='http://192.168.10.10:8080'
ENV SECRET_KEY='sk_fYVw52zywDRVAgsC8yUi2TXFRu1MmtPK'

ENV NAME World

# Run the command to start the order.py script
CMD ["python", "product.py"]
