#! /bin/bash
echo """
==================================================
  Creating certificate for streaming-service
==================================================
"""
mkcert streaming-service

echo """
==================================================
  Copying streaming-service certificates to ./streaming-service/certs
==================================================
"""

mv ./streaming-service.pem ./streaming-service/certs
mv ./streaming-service-key.pem ./streaming-service/certs


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
