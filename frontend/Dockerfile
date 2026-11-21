
FROM nginx:alpine

# Remove default Nginx page
RUN rm -rf /usr/share/nginx/html/*

# Copy frontend files
COPY . /usr/share/nginx/html/

# Expose Nginx port
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
