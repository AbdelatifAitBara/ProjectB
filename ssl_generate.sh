#!/bin/bash

# Variables
key_path="/home/vagrant/ssl/private.key"
crt_path="/home/vagrant/ssl/certificate.crt"
days=365
rsa_key_size=2048

# Generate SSL certificate
openssl req -x509 -nodes -days "$days" -newkey rsa:"$rsa_key_size" -keyout "$key_path" -out "$crt_path" \
    -subj "/C=FR/ST=France/L=Lyon/O=ITS GROUP/CN=ITSGROUP.COM"