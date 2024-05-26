#!/bin/bash

docker run \
  --rm \
  -v $PWD/:/app \
  -w /app \
  python:3.12.3-slim sh -c "pip install jwcrypto && python ./scripts/jwk/create_jwk_invitation.py > ./src/public/.well-known/jwks_invitation.json"