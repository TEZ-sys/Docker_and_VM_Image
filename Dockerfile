FROM nginx:latest
ARG BUILD_ID
LABEL build_id=$BUILD_ID
EXPOSE 80

RUN apt-get install && apt-get install -y python3.5

CMD ["nginx", "-g", "daemon off;"]
