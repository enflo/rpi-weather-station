#!/bin/bash

# Define paths
SERVICE_FILE="weather.station.service"
INSTALL_PATH="/etc/systemd/system/$SERVICE_FILE"
PROJECT_DIR=$(pwd)
PYTHON_PATH=$(which python3)

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit 1
fi

echo "Installing Weather Station Service..."

# Check if service file exists
if [ ! -f "scripts/$SERVICE_FILE" ]; then
    echo "Error: Service file not found at scripts/$SERVICE_FILE"
    exit 1
fi

# Create a temporary service file with correct paths
echo "Configuring service file..."
sed -e "s|<python3_path>|$PYTHON_PATH|g" \
    -e "s|<file_path>|$PROJECT_DIR|g" \
    "scripts/$SERVICE_FILE" > "/tmp/$SERVICE_FILE"

# Move to systemd directory
echo "Copying to systemd..."
mv "/tmp/$SERVICE_FILE" "$INSTALL_PATH"

# Reload systemd
echo "Reloading systemd..."
systemctl daemon-reload

# Enable service
echo "Enabling service..."
systemctl enable "$SERVICE_FILE"

echo "Installation complete!"
echo "You can start the service with: sudo systemctl start $SERVICE_FILE"
