FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY product.py /app
COPY requirements.txt /app
COPY .env /app


RUN python -c 'from dotenv import load_dotenv; load_dotenv()'

# Define environment variables
ENV MYSQL_DATABASE_USER=${MYSQL_DATABASE_USER}
ENV MYSQL_DATABASE_PASSWORD=${MYSQL_DATABASE_PASSWORD}
ENV MYSQL_DATABASE_DB=${MYSQL_DATABASE_DB}
ENV API_URL=${API_URL}
ENV CONSUMER_KEY=${CONSUMER_KEY}
ENV CONSUMER_SECRET=${CONSUMER_SECRET}
ENV SECRET_KEY=${SECRET_KEY}
ENV NAME=${NAME}

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run the command to start the order.py script
CMD ["python", "product.py"]
