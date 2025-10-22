# Viper Scraper Systemd Service Setup

This project automates the running of the Viper Scraper Python script by using **systemd services** and **timers** to start and stop the script during specified hours of the day. The setup includes service management, timer schedules, and the process to deploy these services on a system running Linux.

### Prerequisites

* **Linux-based system** (Ubuntu, Debian, etc.)
* **Python** environment set up with the required dependencies for the Viper Scraper.
* **root** or **sudo** access to install systemd services and timers.

### Overview

This project includes:

* A **systemd service** (`viper_scraper.service`) to run the Viper Scraper script within a virtual environment.
* A **start timer** (`viper_scraper_start.timer`) that triggers the service at **6 AM** and **6 PM**.
* A **stop timer** (`viper_scraper_stop.timer`) that stops the service at **12 Noon** and **12 Midnight**.

### File Structure

```plaintext
ViperScraper/
├── start_viper.sh                   # Shell script to activate virtualenv and run the Python script
├── viper_scraper.py                 # Main Python scraper script
├── systemd_services/                # Directory containing the service and timer files
│   ├── viper_scraper.service        # Systemd service to start the Python script
│   ├── viper_scraper_start.timer    # Timer to start the service at 6 AM & 6 PM
│   ├── viper_scraper_stop.timer     # Timer to stop the service at 12 Noon & 12 Midnight
└── setup_services.sh                # Shell script to move files and set up services
```

### Getting Started

Follow these steps to set up the Viper Scraper systemd service and timer:

1. **Clone the Repository** (if applicable):

   If you haven't already cloned the repository, run:

   ```bash
   git clone https://github.com/gitgyana/ViperScraper.git
   cd ViperScraper
   ```

2. **Install Python Dependencies** (if not done yet):

   Make sure you have the virtual environment set up with all the required Python dependencies for the Viper Scraper.

   ```bash
   python3 -m venv scraperEnv
   source scraperEnv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the Setup Script**:

   The `setup_services.sh` script will automate the setup of the systemd services and timers. This will move the `.service` and `.timer` files to the appropriate directory (`/etc/systemd/system/`), reload systemd, enable the services to run at boot, and start them immediately.

   ```bash
   sudo ./setup_services.sh
   ```

   This script performs the following tasks:

   * Moves the `.service` and `.timer` files to `/etc/systemd/system/`
   * Reloads systemd to register the new files
   * Enables and starts the `viper_scraper.service`, `viper_scraper_start.timer`, and `viper_scraper_stop.timer`
   * Displays the logs of the `viper_scraper.service` to verify everything is working correctly

4. **Check the Status of Services and Timers**:

   After running the setup script, you can check the status of the service and timers:

   ```bash
   sudo systemctl status viper_scraper.service
   sudo systemctl status viper_scraper_start.timer
   sudo systemctl status viper_scraper_stop.timer
   ```

5. **View Logs**:

   To check the logs of the `viper_scraper.service`:

   ```bash
   journalctl -u viper_scraper.service
   ```

   This will show any errors, output, or other details that can help you debug if needed.

### Timers

* **viper_scraper_start.timer**:

  * Starts the `viper_scraper.service` at **6 AM** and **6 PM** every day.

* **viper_scraper_stop.timer**:

  * Stops the `viper_scraper.service` at **12 Noon** and **12 Midnight** every day.

This means the scraper script will only run during the specified time windows: **6 AM - 12 Noon** and **6 PM - 12 Midnight**.

### Troubleshooting

* **Service Not Starting**:

  * If the service fails to start, check the logs for detailed error messages:

    ```bash
    journalctl -u viper_scraper.service
    ```

* **Timer Not Triggering**:

  * Check if the timers are active:

    ```bash
    sudo systemctl list-timers
    ```
  * Ensure that the system time matches the expected schedule and that systemd timers are properly enabled.

* **Permission Issues**:

  * Make sure the `.service` and `.timer` files are correctly moved to `/etc/systemd/system/` and that they have the right ownership.

### Uninstalling or Removing the Service

If you wish to remove the service and timers:

1. Stop and disable the service and timers:

   ```bash
   sudo systemctl stop viper_scraper.service
   sudo systemctl stop viper_scraper_start.timer
   sudo systemctl stop viper_scraper_stop.timer
   ```

2. Disable the services from starting at boot:

   ```bash
   sudo systemctl disable viper_scraper.service
   sudo systemctl disable viper_scraper_start.timer
   sudo systemctl disable viper_scraper_stop.timer
   ```

3. Remove the `.service` and `.timer` files:

   ```bash
   sudo rm /etc/systemd/system/viper_scraper.service
   sudo rm /etc/systemd/system/viper_scraper_start.timer
   sudo rm /etc/systemd/system/viper_scraper_stop.timer
   ```

4. Reload systemd to apply the changes:

   ```bash
   sudo systemctl daemon-reload
   ```

### PS

This setup allows you to run the **Viper Scraper** in a controlled environment using **systemd services and timers**. The script ensures the scraper only runs during certain times of the day, helping automate the process without manual intervention.

---

Feel free to adjust the timings, script, or service settings as needed. If you encounter any issues, check the logs or feel free to reach out for more help!
