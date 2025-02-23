FROM nginx:latest

# Copy nginx conf and SSL files
COPY nginx.conf /etc/nginx/nginx.conf.template
COPY ssl/ssl_cert.crt /etc/nginx/ssl/ssl_cert.crt
COPY ssl/ssl_cert.key /etc/nginx/ssl/ssl_cert.key

# Install envsubst
RUN apt-get update && apt-get install -y gettext-base

# Create start script with all environment variables
RUN echo '#!/bin/sh\n\
envsubst "\$PROJECT_URL \$PROJECT_NAME \$PROJECT_CODENAME \$BACKEND_PORT \$FRONTEND_PORT" < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf\n\
exec nginx -g "daemon off;"' > /docker-entrypoint.sh \
    && chmod +x /docker-entrypoint.sh

# Use the start script as entrypoint
ENTRYPOINT ["/docker-entrypoint.sh"]

