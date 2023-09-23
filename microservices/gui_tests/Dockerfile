# Use a minimal base image
FROM python:3.9-alpine AS base

# Set the working directory to /tests
WORKDIR /tests

# Copy test files from current contents into the container
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Set the working directory to /tests
WORKDIR /tests
COPY test* /tests/

# Create /app directory inside /tests
WORKDIR /tests/app

# Copy my application for test into /app
COPY /gui/app /tests/app/

# Return to directory with test files to launch tests
WORKDIR /tests

# Run the command to start tests "test_app.py", "test_functions.py"
CMD ["python", "test_app.py"]



