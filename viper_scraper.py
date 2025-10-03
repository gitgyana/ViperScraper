import driver_config
from forum_scraper import ForumScraper
from data_exporter import DataExporter


globals().update(driver_config.libs)


def main():
    """
    Executes the primary workflow of the program.
    """
    driver = driver_config.driver
    wait = WebDriverWait(driver, 10)

    scraper = ForumScraper(driver, wait)

    try:
        base_url = input("Enter site \n > ")

        scraper.scrape_all_pages(base_url=base_url, page_count=1)

        saver = DataExporter(filename='scraped_forum')
        saver.save(scraper.forum_data)
        
    except Exception as e:
        print(f"Error in main: {e}")
    finally:
        scraper.close()


if __name__ == '__main__':
	main()