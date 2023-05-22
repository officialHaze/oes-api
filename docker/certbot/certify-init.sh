#!/bin/sh

set -e

until nc -z proxy 80; do
    echo "waiting for proxy..."
    sleep 5s & ${!}
done

echo "Getting certificate"

certbot certonly \
    --webroot \
    --webroot-path "/vol/www/" \
    -d "$DOMAIN" \
    --email $EMAIL \
    --rsa-key-size 4096 \
    --agree-tos \
    --noninteractive

