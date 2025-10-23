#!/bin/bash

SOURCE_DIR="./systemd_services"
DEST_DIR="/etc/systemd/system"

echo "Moving .service and .timer files to $DEST_DIR..."
sudo mv $SOURCE_DIR/*.service $DEST_DIR/
sudo mv $SOURCE_DIR/*.timer $DEST_DIR/

echo "Stop and disable existing viper services and timers"

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
