import driver_config
from site_list import urls
from forum_scraper import ForumScraper
from data_exporter import DataExporter
from logger import log


globals().update(driver_config.libs)


def main():
    """
    Executes the primary workflow of the program.
    """
    driver = driver_config.driver
    wait = WebDriverWait(driver, 10)

    scraper = ForumScraper(driver, wait)

    try:
        sl = 0
        while True:
            log("info", f"URL[{sl}]: {urls[sl]}")
            scraper.scrape_all_pages(base_url=urls[sl], page_count=10)
            
            saver = DataExporter(filename='scraped_forum', mode='sqlite')
            saver.save(data=scraper.forum_data, mode='sqlite')

            scraper.forum_data = []
            
            sl += 1
            if sl >= len(urls):
                sl = 0
        
    except Exception as e:
        log("error", f"Error in main: {e}")
    finally:
        scraper.close()


if __name__ == '__main__':
    main()
