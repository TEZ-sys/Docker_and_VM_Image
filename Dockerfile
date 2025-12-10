FROM ubuntu:22.04

RUN apt-get update && apt-get install -y nginx && apt-get install -y python3.5
RUN echo "<h1>Welcome to DevOps DDoS Protection System</h1>"  >> /var/www/html/index.html
ARG BUILD_ID
LABEL build_id=$BUILD_ID
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
