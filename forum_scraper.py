import time

import driver_config


globals().update(driver_config.libs)


class ForumScraper:
    """Scrapes data from a forum using Selenium."""

    def __init__(self):
        """
        Initialize the ForumScraper instance.
        """
        self.driver = driver_config.driver
        self.wait = WebDriverWait(self.driver, 10)
        self.popup_script = ""
        self.forum_data = []

    def show_popup_notification(self, message):
        """
        Show popup notification on the rendered site
        """
        with open("notify.js", "r", encoding="utf-8") as file:
            self.popup_script = file.read().strip().replace("py__message__", message)

        try:
            self.driver.execute_script(popup_script)
            time.sleep(1)
        except Exception as e:
            print(f"Could not show popup: {e}")


def main():
	"""
	Main entry point of the script.
    Executes the primary workflow of the program.
    """
	scraper = ForumScraper()


if __name__ == "__main__":
    main()
