import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

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
            self.driver.execute_script(self.popup_script)
            time.sleep(1)
        except Exception as e:
            print(f"Could not show popup: {e}")

    def scrape_all_pages(self, base_url=None	, start_page=1, max_pages=None):
        """
        Scrape all pages starting from start_page
        """
        if not base_url:
        	base_url = input("Enter forum url \n > ")

        try:
            first_url = f"{base_url}/page{start_page}"
            self.driver.get(first_url)

            self.show_popup_notification("Starting forum scraping process")
            time.sleep(2)

            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            time.sleep(30)

            print(f"Scraping completed. Total posts collected: {len(self.forum_data)}")

        except Exception as e:
            print(f"Error during scraping: {e}")


def main():
	"""
	Main entry point of the script.
    Executes the primary workflow of the program.
    """
	scraper = ForumScraper()


if __name__ == "__main__":
    main()
