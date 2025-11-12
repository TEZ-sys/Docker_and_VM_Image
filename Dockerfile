FROM nginx:latest
#Added small text to trigger pipeline workflow 
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
