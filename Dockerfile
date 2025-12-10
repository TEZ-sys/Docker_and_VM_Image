FROM ubuntu:22.02

RUN apt-get install -y nginx
RUN echo "<h1>Welcome to DevOps DDoS Protection System</h1>"  >> /var/www/html/index.html
ARG BUILD_ID
LABEL build_id=$BUILD_ID
EXPOSE 80

RUN apt-get install && apt-get install -y python3.5
RUN python --version

CMD ["nginx", "-g", "daemon off;"]
