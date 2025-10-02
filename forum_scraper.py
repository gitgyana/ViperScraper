import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

import driver_config
from post_scraper import PostScraper


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

    def get_max_page_number(self, soup):
        """
        Extract maximum page number from pagination
        """
        try:
            pagination = soup.find('div', {'id': 'pagination_top'})
            if not pagination:
                return 1

            page_info = pagination.find('span').find('a', class_='popupctrl')
            if page_info:
                text = page_info.get_text(strip=True)
                match = re.search(r'Page \d+ of (\d+)', text)
                if match:
                    return int(match.group(1))

            # Alternative
            page_links = pagination.find_all('a', href=re.compile(r'/page\d+'))
            max_page = 1
            for link in page_links:
                href = link.get('href', '')
                page_match = re.search(r'/page(\d+)', href)
                if page_match:
                    page_num = int(page_match.group(1))
                    max_page = max(max_page, page_num)

            return max_page

        except Exception as e:
            print(f"Error getting max page number: {e}")
            return 1

    def extract_forum_info(self, soup):
        """
        Extract forum name and link
        """
        try:
            pagetitle = soup.find('div', {'id': 'pagetitle'})
            if pagetitle:
                thread_title = pagetitle.find('span', class_='threadtitle')
                if thread_title:
                    forum_name = thread_title.find('a').get_text(strip=True)
                    forum_link = thread_title.find('a').get('href', '')
                    return forum_name, forum_link
        except Exception as e:
            print(f"Error extracting forum info: {e}")

        return "Unknown Forum", ""

    def scrape_page(self, url):
        """
        Scrape a single page
        """
        try:
            print(f"Scraping page: {url}")
            self.driver.get(url)

            self.show_popup_notification("Going to process task")

            self.wait.until(EC.presence_of_element_located((By.ID, "postlist")))

            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            forum_name, forum_link = self.extract_forum_info(soup)
            
            post_scraper = PostScraper(forum_name, forum_link)
            page_data = post_scraper.find_posts(soup)

            return page_data

        except Exception as e:
            print(f"Error scraping page {url}: {e}")
            return []

    def scrape_all_pages(self, base_url=None, start_page=1, max_pages=None):
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

            if max_pages is None:
                max_page_num = self.get_max_page_number(soup)
                print(f"Detected maximum page number: {max_page_num}")
            else:
                max_page_num = max_pages

            current_page = max_page_num - 10

            while current_page <= max_page_num:
                page_url = f"{base_url}/page{current_page}"
                page_data = self.scrape_page(page_url)
                self.forum_data.extend(page_data)

                print(f"Completed page {current_page}/{max_page_num}. Total posts collected: {len(self.forum_data)}")

                current_page += 1
                time.sleep(2)

            print(f"Scraping completed. Total posts collected: {len(self.forum_data)}")

        except Exception as e:
            print(f"Error during scraping: {e}")

    def close(self):
        """
        Close the webdriver
        """
        if self.driver:
            self.driver.quit()


def main():
	"""
	Main entry point of the script.
    Executes the primary workflow of the program.
    """
	scraper = ForumScraper()


if __name__ == "__main__":
    main()
