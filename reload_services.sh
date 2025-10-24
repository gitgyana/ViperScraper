#!/bin/bash

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
