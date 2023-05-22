#!/bin/bash

set -e 

echo "Checking for dhparams...."
if [ ! -f "/vol/proxy/ssl-dhparams.pem" ]; then
    echo "dhparams.pem does not exist.....creating it..."
    openssl dhparams -out /vol/proxy/ssh-dhparams.pem 2048
    echo "dhparams.pem created"
fi

# Avoiding replacing these with envsubstr
export host=\$host
export request_uri=\$request_uri

echo "Checking for fullchain.pem"
if [! -f "/etc/letsencrypt/live/${DOMAIN}/fullchain.pem"]; then
    echo "no SSL cert found....enabling HTTP!"
    envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf
else
    echo "SSL cert found....enabling HTTPS!"
    envsubst < /etc/nginx/default-ssl.conf.tpl > /etc/nginx/conf.d/default.conf
fi

nginx -g "daemon off;"
