#!/bin/bash

LOG_DIR="/home/debian/Projects/ViperScraper/logs"
LOG_FILE="$LOG_DIR/start_viper.log"

mkdir -p $LOG_DIR

source /home/debian/Projects/ViperScraper/scraperEnv/bin/activate

echo "Starting Viper Scraper..." >> $LOG_FILE
echo "Activating virtual environment..." >> $LOG_FILE

python /home/debian/Projects/ViperScraper/viper_scraper.py

echo "Viper scraper script finished"
