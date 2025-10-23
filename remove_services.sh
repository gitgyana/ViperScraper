#!/bin/bash

echo "Stop and disable existing viper services and timers"

sudo systemctl stop viper_scraper.service
sudo systemctl disable viper_scraper.service

sudo systemctl stop viper_scraper_start.timer
sudo systemctl disable viper_scraper_start.timer

sudo systemctl stop viper_scraper_stop.timer
sudo systemctl disable viper_scraper_stop.timer


sudo systemctl status viper_scraper.service
sudo systemctl status viper_scraper_start.timer
sudo systemctl status viper_scraper_stop.timer
