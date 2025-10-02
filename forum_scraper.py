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
        self.forum_data = []


def main():
	"""
	Main entry point of the script.
    Executes the primary workflow of the program.
    """
	scraper = ForumScraper()
	# test
	scraper.driver.get("https://www.google.com/")
	time.sleep(20)


if __name__ == "__main__":
    main()
