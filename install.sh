#!/bin/bash

# KINSTALLER SCRIPT FOR KBACK

pacman -S --needed python3 python-pip python-tqdm tar

# Check if running as root
if [ "$(id -u)" -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

# Move the script to /usr/bin/ and make it executable
touch /usr/bin/kback
cp kback.py /usr/bin/kback
chmod +x /usr/bin/kback

# Making Config File
# Check if the directory exists
if [ ! -d "/etc/kback" ]; then
  # Directory does not exist, create it
  mkdir -p "/etc/kback"
  touch /etc/kback/kback.conf
  cp ./kback.conf /etc/kback/kback.conf
fi


# This will only show if it installed right (not much can really go wrong ngl)
echo ""
echo ""
echo ""
echo ""
echo "kback installed successfully"
echo ""
echo "It is not recommended to save backups to the default location."
echo "To change the location of saved backups"
echo "Edit /etc/kback/kback.conf"