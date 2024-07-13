#!/bin/bash

# Check if the script is running as sudo
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root."
   exit 1
fi

# Define variables
NGINX_CONF_D="/etc/nginx/conf.d"
FLASK_APP_NAME="mail_sender_app" 
FLASK_HOST="127.0.0.1"
FLASK_PORT="5000"

# Create a new nginx configuration file
cat <<EOF > "${NGINX_CONF_D}/${FLASK_APP_NAME}.conf"
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://${FLASK_HOST}:${FLASK_PORT};
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    access_log /var/log/nginx/${FLASK_APP_NAME}_access.log;
    error_log /var/log/nginx/${FLASK_APP_NAME}_error.log;
}
EOF

# Test nginx configuration
nginx -t

# If test passes, reload nginx to apply changes
if [ $? -eq 0 ]; then
    systemctl reload nginx
    echo "Nginx configuration reloaded successfully."
else
    echo "Nginx configuration test failed. Please check your configuration."
fi

