#!/bin/bash

SOURCE_DIR="./systemd_services"
DEST_DIR="/etc/systemd/system"

echo "Copying .service and .timer files to $DEST_DIR..."
sudo cp $SOURCE_DIR/*.service $DEST_DIR/
sudo cp $SOURCE_DIR/*.timer $DEST_DIR/
STATUS=$?

if [ $STATUS -eq 0 ]; then
    echo "Done"
else
    echo "ERROR"
fi
