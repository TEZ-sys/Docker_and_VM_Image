FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y nginx curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
    
RUN echo "<h1>Welcome to DevOps DDoS Protection System</h1>"  >> /var/www/html/index.html
COPY math_test.py /usr/local/bin/math_test.py

RUN chmod +x /usr/local/bin/math_test.py

ARG BUILD_ID
LABEL build_id=$BUILD_ID
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
