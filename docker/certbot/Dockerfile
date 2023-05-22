FROM certbot/certbot:v1.27.0
LABEL maintainer="Moinak Dey"

COPY ./certify-init.sh /opt/

RUN chmod +x /opt/certify-init.sh

ENTRYPOINT []
CMD [ "certbot", "renew" ]

