#!/bin/bash
echo "Starting Viper Scraper" >> /home/debian/Projects/ViperScraper/start_viper.log
echo "Activating virtual environment..." >> /home/debian/Projects/ViperScraper/start_viper.log
source /home/debian/Projects/ViperScraper/scraperEnv/bin/activate
echo "Virtual environment activated" >> /home/debian/Projects/ViperScraper/start_viper.log
python /home/debian/Projects/ViperScraper/viper_scraper.py >> /home/debian/Projects/ViperScraper/start_viper.log 2>&1
echo "Viper scraper script finished" >> /home/debian/Projects/ViperScraper/start_viper.log
