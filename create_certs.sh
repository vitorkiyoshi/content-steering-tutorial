#! /bin/bash
echo """
==================================================
  Creating certificate for streaming-service.localhost
==================================================
"""
mkcert streaming-service

echo """
==================================================
  Copying streaming-1.localhost certificates to ./streaming-1/certs
==================================================
"""

mv ./streaming-service.pem ./streaming-service/certs
mv ./streaming-service-key.pem ./streaming-service/certs


