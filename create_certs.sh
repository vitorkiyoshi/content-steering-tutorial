#! /bin/bash
echo """
==================================================
  Creating certificate for streaming-1.localhost
==================================================
"""
mkcert streaming-service.localhost

echo """
==================================================
  Copying streaming-1.localhost certificates to ./streaming-1/certs
==================================================
"""

mv ./streaming-service.localhost.pem ./streaming-service/certs
mv ./streaming-service.localhost-key.pem ./streaming-service/certs


