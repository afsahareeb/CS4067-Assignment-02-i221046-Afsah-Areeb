# Use Nginx as the base image
FROM nginx:alpine

# Remove default Nginx config and use custom one
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Set working directory inside the container
WORKDIR /usr/share/nginx/html

# Copy frontend files (HTML, CSS, JS) to Nginx's default location
COPY . .

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
