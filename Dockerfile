FROM nginx:latest
ARG BUILD_ID
LABEL build_id=$BUILD_ID
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
