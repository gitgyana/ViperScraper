#!/bin/bash

PROJECT_DIR="$(dirname "$(realpath "$0")")"

VENV_DIR="$PROJECT_DIR/scraperEnv"
LOGS_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOGS_DIR/start_viper.log"

if [ ! -d "$LOGS_DIR" ]; then
    echo "Creating logs directory..." >> "$LOG_FILE"
    mkdir -p "$LOGS_DIR"
fi

echo "Starting Viper Scraper" >> "$LOG_FILE"

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..." >> "$LOG_FILE"
    python3 -m venv "$VENV_DIR"
    echo "Virtual environment created" >> "$LOG_FILE"

    source "$VENV_DIR/bin/activate"
    echo "Installing requirements..." >> "$LOG_FILE"
    pip install -r "$PROJECT_DIR/requirements.txt" >> "$LOG_FILE" 2>&1
    echo "Requirements installed" >> "$LOG_FILE"
else
    echo "Activating existing virtual environment..." >> "$LOG_FILE"
    source "$VENV_DIR/bin/activate"
    echo "Virtual environment activated" >> "$LOG_FILE"
fi

echo "Running Viper scraper script..." >> "$LOG_FILE"
python "$PROJECT_DIR/viper_scraper.py" >> "$LOG_FILE" 2>&1

echo "Viper scraper script finished" >> "$LOG_FILE"
