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
        for base_url in urls:
            scraper.scrape_all_pages(base_url=base_url, page_count=1)

            saver = DataExporter(filename='scraped_forum')
            saver.save(scraper.forum_data)

            scraper.forum_data = []
        
    except Exception as e:
        log("error", f"Error in main: {e}")
    finally:
        scraper.close()


if __name__ == '__main__':
	main()