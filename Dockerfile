# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY product.py /app
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variables
ENV CONSUMER_KEY=ck_c86d458381c645d1709dbbf95ae3033226871df8
ENV CONSUMER_SECRET=cs_a413d091ad0ebc09df06e547dcbb787e0256baeb

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "product.py"]