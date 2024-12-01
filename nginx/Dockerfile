FROM nginx:latest

RUN apt-get update && apt-get install -y openssl

RUN mkdir -p /etc/nginx/certs

RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/certs/localhost.key \
    -out /etc/nginx/certs/localhost.crt \
    -subj "/C=ID/ST=Jakarta/L=SouthJakarta/O=MyCompany/CN=localhost"

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80 443
