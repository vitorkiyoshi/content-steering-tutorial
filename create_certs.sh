#! /bin/bash
echo """
==================================================
  Creating certificate for $1
==================================================
"""
mkcert $1

echo """
==================================================
  Copying $1 certificates to ./$1/certs
==================================================
"""

mv ./$1.pem ./$1/certs
mv ./$1-key.pem ./$1/certs


echo """
==================================================
  Creating certificate for steering-service
==================================================
"""
mkcert steering-service

echo """
==================================================
  Copying steering-service certificates to ./steering-service/certs
==================================================
"""

mv ./steering-service.pem ./steering-service/certs
mv ./steering-service-key.pem ./steering-service/certs
