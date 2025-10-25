#!/bin/bash

echo "Stop and disable existing viper services and timers"

systemctl stop viper_scraper.service
systemctl disable viper_scraper.service

systemctl stop viper_scraper_start.timer
systemctl disable viper_scraper_start.timer

systemctl status viper_scraper.service
systemctl status viper_scraper_start.timer
