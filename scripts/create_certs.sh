#!/bin/bash

openssl genrsa -out ./certs/private_invitation.pem 3072
openssl rsa -in ./certs/private_invitation.pem -pubout -out ./certs/public_invitation.pem