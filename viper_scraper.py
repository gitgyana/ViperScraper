import time

import driver_config as config
from forum_scraper import ForumScraper
from data_exporter import DataExporter
from logger import log


globals().update(config.libs)


def main():
    """
    Executes the primary workflow of the program.
    """
    urls = []
    file_path = "site_list.txt"
    
    try:
        with open(file_path, 'r') as file:
            urls = [line.strip() for line in file]

    except Exception as file_err:
        log("error", f"Error FILE TO LIST: {file_err}")

    try:
        for sl in range(0, len(urls)):
            driver = None
            try:
                driver = config.create_driver()
                wait = WebDriverWait(driver, 10)
                scraper = ForumScraper(driver, wait)
            except Exception as e:
                log("error", f"Error in main driver creation: {e}")
            
            log("info", f"URL[{sl} / {len(urls) - 1}]: {urls[sl]}")
            scraper.scrape_all_pages(base_url=urls[sl], page_count=10)
            
            saver = DataExporter(filename='scraped_forum')
            saver.save(data=scraper.forum_data, mode='sqlite')

            scraper.forum_data = []
            
            try:
                driver.quit()
            except Exception as last_err:
                log("error", f"Error in main driver quit: {e}")
            finally:
                time.sleep(60)
            
    except Exception as e:
        log("error", f"Error in main: {e}")


if __name__ == '__main__':
    main()
