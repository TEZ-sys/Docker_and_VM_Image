FROM alpine:3.21

RUN apk add --no-cache nginx curl python3

RUN echo "<h1>Welcome to DevOps DDoS Protection System</h1>" >> /usr/share/nginx/html/index.html

COPY math_test.py /usr/local/bin/math_test.py
RUN chmod +x /usr/local/bin/math_test.py

ARG BUILD_ID
LABEL build_id=$BUILD_ID

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
