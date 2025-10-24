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
        sl = 0
        while True:
            driver = config.create_driver()
            wait = WebDriverWait(driver, 10)

            scraper = ForumScraper(driver, wait)

            
            log("info", f"URL[{sl}]: {urls[sl]}")
            scraper.scrape_all_pages(base_url=urls[sl], page_count=10)
            
            saver = DataExporter(filename='scraped_forum')
            saver.save(data=scraper.forum_data)

            scraper.forum_data = []
            
            sl += 1
            if sl >= len(urls):
                sl = 0

            scraper.close()
            time.sleep(30)

    except Exception as e:
        log("error", f"Error in main: {e}")


if __name__ == '__main__':
    main()
