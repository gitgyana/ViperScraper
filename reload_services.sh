#!/bin/bash

echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "Enabling and starting viper_scraper.service..."
systemctl enable viper_scraper.service
systemctl start viper_scraper.service

echo "Enabling and starting viper_scraper_start.timer..."
systemctl enable viper_scraper_start.timer
systemctl start viper_scraper_start.timer

echo "Displaying logs for viper_scraper.service..."
journalctl -u viper_scraper.service
