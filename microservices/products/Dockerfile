FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY product.py /app
COPY requirements.txt /app
COPY zabbix_agentd.conf /etc/zabbix/zabbix_agentd.conf

# Install required dependencies
RUN apt-get update && apt-get install -y wget

# Download Zabbix agent package
RUN wget https://repo.zabbix.com/zabbix/5.4/debian/pool/main/z/zabbix-release/zabbix-release_5.4-1+debian10_all.deb

# Install Zabbix agent package
RUN dpkg -i zabbix-release_5.4-1+debian10_all.deb && apt-get update && apt-get install -y zabbix-agent

# Install any other needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variables
ENV API_URL='http://192.168.10.10:8888/wp-json/wc/v3/products'
ENV CONSUMER_KEY='ck_0ef13b972c2c516f8882152bdc8f18cdcde15241'
ENV CONSUMER_SECRET='cs_9b72ab7e203b93fe600b747fb71367b504b51eac'
ENV SECRET_KEY='sk_fYVw52zywDRVAgsC8yUi2TXFRu1MmtPK'
ENV NAME World

# Start Zabbix agent service and run the command to start the product.py script
CMD service zabbix-agent start && python product.py