#!/bin/bash

SOURCE_DIR="./systemd_services"
DEST_DIR="/etc/systemd/system"

echo "Copy .service and .timer files to $DEST_DIR..."
sudo cp $SOURCE_DIR/*.service $DEST_DIR/
sudo cp $SOURCE_DIR/*.timer $DEST_DIR/

echo "Make the start_viper.sh script executable..."
chmod +x /home/debian/Projects/ViperScraper/start_viper.sh

echo "Make script readable and executable by everyone..."
chmod 755 /home/debian/Projects/ViperScraper/start_viper.sh

echo "Stop and disable existing viper services and timers..."
systemctl stop viper_scraper.service
systemctl disable viper_scraper.service

systemctl stop viper_scraper_start.timer
systemctl disable viper_scraper_start.timer

echo "Reloading systemd daemon..."
systemctl daemon-reload

echo "Enabling and starting viper_scraper.service..."
systemctl enable viper_scraper.service
systemctl start viper_scraper.service

echo "Enabling and starting viper_scraper_start.timer..."
systemctl enable viper_scraper_start.timer
systemctl start viper_scraper_start.timer

echo "Displaying logs for viper_scraper.service..."
journalctl -u viper_scraper.service
