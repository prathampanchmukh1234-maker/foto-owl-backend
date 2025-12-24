FROM nginx:alpine

RUN rm -rf /usr/share/nginx/html/*

# Force copy using absolute repo paths
COPY ./frontend/index.html /usr/share/nginx/html/index.html
COPY ./frontend/script.js /usr/share/nginx/html/script.js
COPY ./frontend/style.css /usr/share/nginx/html/style.css

# Force nginx config
COPY ./frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
