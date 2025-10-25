import time

import driver_config as config
from site_list import urls
from forum_scraper import ForumScraper
from data_exporter import DataExporter
from logger import log


globals().update(config.libs)


def main():
    """
    Executes the primary workflow of the program.
    """
    try:
        for sl in range(0, len(urls)):
            driver = config.create_driver()
            wait = WebDriverWait(driver, 10)

            scraper = ForumScraper(driver, wait)

            
            log("info", f"URL[{sl} / {len(urls) - 1}]: {urls[sl]}")
            scraper.scrape_all_pages(base_url=urls[sl], page_count=10)
            
            saver = DataExporter(filename='scraped_forum')
            saver.save(data=scraper.forum_data)

            scraper.forum_data = []
            
            driver.quit()
            time.sleep(10)

    except Exception as e:
        log("error", f"Error in main: {e}")


if __name__ == '__main__':
    main()
