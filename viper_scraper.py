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
        driver = config.create_driver()
        wait = WebDriverWait(driver, 10)
        scraper = ForumScraper(driver, wait)
    except Exception as e:
        log("error", f"Error in main driver creation: {e}")
            
    try:
        for sl in range(0, len(urls)):
            log("info", f"URL[{sl} / {len(urls) - 1}]: {urls[sl]}")
            scraper.scrape_all_pages(base_url=urls[sl], page_count=10)
            
            saver = DataExporter(filename='scraped_forum')
            saver.save(data=scraper.forum_data)

            scraper.forum_data = []
            
    except Exception as e:
        log("error", f"Error in main: {e}")
    finally:
        try:
            driver.quit()
        except Exception as last_err:
            log("error", f"Error in main driver quit: {e}")
            
        time.sleep(10)


if __name__ == '__main__':
    main()
