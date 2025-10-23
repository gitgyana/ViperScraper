#!/bin/bash

SOURCE_DIR="./systemd_services"
DEST_DIR="/etc/systemd/system"

echo "Copy .service and .timer files to $DEST_DIR..."
sudo cp $SOURCE_DIR/*.service $DEST_DIR/
sudo cp $SOURCE_DIR/*.timer $DEST_DIR/

echo "Make the start_viper.sh script executable..."
chmod +x /home/debian/Projects/ViperScraper/start_viper.sh

echo "Make script readable and executable by everyone..."
sudo chmod 755 /home/debian/Projects/ViperScraper/start_viper.sh

echo "Stop and disable existing viper services and timers..."
sudo systemctl stop viper_scraper.service
sudo systemctl disable viper_scraper.service

sudo systemctl stop viper_scraper_start.timer
sudo systemctl disable viper_scraper_start.timer

sudo systemctl stop viper_scraper_stop.timer
sudo systemctl disable viper_scraper_stop.timer

echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "Enabling and starting viper_scraper.service..."
sudo systemctl enable viper_scraper.service
sudo systemctl start viper_scraper.service

echo "Enabling and starting viper_scraper_start.timer..."
sudo systemctl enable viper_scraper_start.timer
sudo systemctl start viper_scraper_start.timer

echo "Enabling and starting viper_scraper_stop.timer..."
sudo systemctl enable viper_scraper_stop.timer
sudo systemctl start viper_scraper_stop.timer

echo "Displaying logs for viper_scraper.service..."
journalctl -u viper_scraper.service
