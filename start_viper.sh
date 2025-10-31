#!/bin/bash

LOG_DIR="/home/debian/Projects/ViperScraper/logs"
LOG_FILE="$LOG_DIR/start_viper.log"

mkdir -p $LOG_DIR

echo "Activating virtual environment..." >> $LOG_FILE
source /home/debian/Projects/ViperScraper/scraperEnv/bin/activate

echo "$(date '+%Y-%m-%d %H:%M:%S') - Starting Viper Scraper..." >> "$LOG_FILE"

python /home/debian/Projects/ViperScraper/oneshot_viper.py
STATUS=$?

if [ $STATUS -eq 0 ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Viper Scraper finished successfully." >> "$LOG_FILE"
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Viper Scraper FAILED with code $STATUS." >> "$LOG_FILE"
fi

deactivate
