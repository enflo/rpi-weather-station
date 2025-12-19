#!/bin/bash

set -e

echo "Starting system setup for RPi Weather Station..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit 1
fi

echo "Updating package lists..."
apt-get update

echo "Installing system dependencies..."
# Core Python and build tools
# python3-full includes venv on some distros, python3-dev for building C extensions
apt-get install -y python3-full python3-pip python3-dev python3-venv build-essential

# Hardware interfaces
apt-get install -y i2c-tools python3-smbus libgpiod-dev

# Database dependencies (for psycopg2)
apt-get install -y libpq-dev

# Git (usually present, but good to ensure)
apt-get install -y git

# Enable I2C interface if not enabled
if grep -q "dtparam=i2c_arm=on" /boot/config.txt; then
    echo "I2C is already enabled in config.txt"
else
    echo "Enabling I2C in /boot/config.txt..."
    echo "dtparam=i2c_arm=on" >> /boot/config.txt
    echo "Note: A reboot will be required for I2C to be active."
fi

# Load I2C module
if ! lsmod | grep -q i2c_dev; then
    echo "Loading i2c-dev module..."
    modprobe i2c-dev
    echo "i2c-dev" >> /etc/modules
fi

echo "System dependencies installed successfully."
echo "Please reboot your Raspberry Pi if you just enabled I2C."
