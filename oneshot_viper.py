import re
import os
import time
import csv
import sqlite3
import requests
import platform
import threading
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from site_list import urls
from logger import log


disable_site_permissions = True
curr_dt = datetime.now().strftime('%Y.%m.%d_%H.%M.%S')


class DataExporter:
    """
    Handles exporting data to CSV, SQLite, or both based on the specified mode
    """

    def __init__(self, mode='*', filename=f'data_{curr_dt}', dirname='ProcessedData', tablename=None):
        """
        Initialize export mode and filename, defaulting to CSV and timestamped name
        """
        self.mode = mode.lower()
        self.filename = filename
        self.tablename = tablename
        self.extn = ''

        if not tablename:
            self.tablename = filename

        if self.mode not in ['csv', 'sqlite3', 'sqlite', 'db', '*']:
            self.mode = '*'

        if not dirname:
            dirname = 'ProcessedData'

        self.filepath = os.path.join(dirname, f"{self.filename}")
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)

    def _save_to_csv(self, data):
        """
        Internal method to save data to a CSV file
        """
        try:
            fieldnames = ''
            if isinstance(data, dict):
                fieldnames = list(data.keys())
            elif isinstance(data[0], dict):
                fieldnames = list(data[0].keys())
            else:
                raise ValueError("Data must be a dict or a list/tuple with a dict as the first element")

            if self.extn != '.csv':
                self.extn = '.csv'

            filepath = self.filepath + self.extn

            if not os.path.isfile(filepath):
                with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()

            existing_rows = set()
            with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    existing_rows.add(tuple(row.items()))

            with open(filepath, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                if isinstance(data, dict):
                    data = [data]

                for post in data:
                    post_copy = post.copy()

                    for key in post_copy:
                        value = post_copy[key]
                        if isinstance(value, (list, tuple, set)):
                            post_copy[key] = '; '.join(str(item) for item in value)
                        else:
                            post_copy[key] = str(value) if value is not None else ''

                    if tuple(post_copy.items()) in existing_rows:
                        continue

                    writer.writerow(post_copy)

            log("info", f"[CSV] Data saved: {filepath}")

        except Exception as e:
            log("error", f"[CSV] Error saving: {e}")

    def _save_to_sqlite(self, data):
        """
        Internal method to save data to a SQLite database file
        """
        conn = None
        try:
            fieldnames = ''
            if isinstance(data, dict):
                fieldnames = list(data.keys())
            elif isinstance(data[0], dict):
                fieldnames = list(data[0].keys())
            else:
                raise ValueError("Data must be a dict or a list/tuple with a dict as the first element")

            if self.extn not in ['.sqlite3', '.sqlite', '.db']:
                self.extn = '.db'

            filepath = self.filepath + self.extn

            conn = sqlite3.connect(filepath)
            cursor = conn.cursor()
            
            # Sanitize tablename
            tablename = ''.join(c if c.isalnum() or c == '_' else '_' for c in self.tablename)
            if not tablename or tablename[0].isdigit():
                tablename = 'data_' + tablename
            
            column_definitions = ', '.join([f'`{field}` TEXT' for field in fieldnames])
            unique_constraint = f', UNIQUE ({", ".join([f"`{field}`" for field in fieldnames])})'
            create_table_query = f'CREATE TABLE IF NOT EXISTS `{tablename}` ({column_definitions}{unique_constraint})'
            cursor.execute(create_table_query)
            
            if isinstance(data, dict):
                data = [data]
            
            for record in data:
                record_copy = record.copy()
                
                for key in record_copy:
                    value = record_copy[key]
                    if isinstance(value, (list, tuple, set)):
                        record_copy[key] = '; '.join(str(item) for item in value)
                    else:
                        record_copy[key] = str(value) if value is not None else ''
                
                column_names = ', '.join([f'`{field}`' for field in fieldnames])
                placeholders = ', '.join(['?' for _ in fieldnames])
                insert_query = f'INSERT OR IGNORE INTO `{tablename}` ({column_names}) VALUES ({placeholders})'
                
                values = [record_copy.get(field, '') for field in fieldnames]
                cursor.execute(insert_query, values)
            
            conn.commit()
            log("info", f"[SQLite] Data saved: {filepath} (table: {tablename})")
            
        except Exception as e:
            log("error", f"[SQLite] Error saving: {e}")
        finally:
            if conn:
                conn.close()

    def save(self, data, mode=None):
        """
        Save the given data in the selected format(s)
        """
        if mode not in ['csv', 'sqlite3', 'sqlite', 'db', '*']:
            self.mode = '*'

        if self.mode in ['csv', '*']:
            self.extn = '.csv'
            self._save_to_csv(data)

        if self.mode in ['sqlite3', 'sqlite', 'db', '*']:
            self.extn = '.db'
            self._save_to_sqlite(data)


class ForumScraper:
    """
    Scrapes data from a forum using Selenium
    """

    def __init__(self, driver=None, wait=None):
        """
        Initialize the ForumScraper instance.
        """
        if driver is None:
            options = webdriver.ChromeOptions()
            self.driver = webdriver.Chrome(options=options)
        else:
            self.driver = driver

        if wait is None:
            self.wait = WebDriverWait(self.driver, 10)
        else:
            self.wait = wait

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
            log("warning", f"Could not show popup: {e}")

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
            log("error", f"Error getting max page number: {e}")
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
            log("error", f"Error extracting forum info: {e}")

        return "Unknown Forum", ""

    def scrape_page(self, url):
        """
        Scrape a single page
        """
        try:
            log("info", f"Scraping page: {url}")
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
            log("error", f"Error scraping page {url}: {e}")
            return []

    def scrape_all_pages(self, base_url=None, start_page=1, max_pages=None, page_count=10):
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
                log("info", f"Detected maximum page number: {max_page_num}")
            else:
                max_page_num = max_pages

            current_page = max_page_num - page_count

            while current_page <= max_page_num:
                page_url = f"{base_url}/page{current_page}"
                page_data = self.scrape_page(page_url)
                self.forum_data.extend(page_data)

                log("info", f"Completed page {current_page}/{max_page_num}. Total posts collected: {len(self.forum_data)}")

                current_page += 1
                time.sleep(2)

            log("info", f"Scraping completed. Total posts collected: {len(self.forum_data)}")

        except Exception as e:
            log("error", f"Error during scraping: {e}")


    def close(self):
        """
        Close the webdriver
        """
        if self.driver:
            self.driver.quit()


class PostScraper:
    """
    Scrapes post data including images and download links from a forum
    """

    def __init__(self, forum_name=None, forum_link=None):
        """
        Initialize host filters and data structures
        """
        self.forum_data = []
        self.img_hosts = ['pixhost.to', 'imgur.com', 'imageban.ru']
        self.file_hosts = ["rapidgator", "katfile", "subyshare", "mexa"] 
        self.img_ext = ('.jpg', '.jpeg', '.png', '.gif')
        self.vid_ext = ('.mp4', '.avi', '.mkv', '.zip', '.rar')
        self.forum_name = forum_name
        self.forum_link = forum_link

    def parse_date(self, date_text):
        """
        Parse date from post format into YYYY.MM.DD format
        """
        try:
            date_text = re.sub(r'\s+', ' ', date_text.strip())
            
            # Handle "Today,HH:MM" and "Yesterday,HH:MM"
            if 'Today' in date_text:
                today = datetime.today()
                return today.strftime('%Y.%m.%d')

            if 'Yesterday' in date_text:
                yesterday = datetime.today() - timedelta(days=1)
                return yesterday.strftime('%Y.%m.%d')

            # Pattern: "30th September 2025"
            date_match = re.search(r'(\d{1,2}\w{0,2}\s+\w+\s+\d{4})', date_text)
            
            if date_match:
                date_str = date_match.group(1)
                
                date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)
                
                try:
                    return datetime.strptime(date_str, '%d %B %Y').strftime('%Y.%m.%d')
                except:
                    return date_str

        except Exception as e:
            log("error", f"Error parsing date: {e}")

        return date_text

    def extract_post_data(self, post_li):
        """
        Extract data and metadata from a post
        """
        try:
            post_data = {}

            # Date and post link
            posthead = post_li.find('div', class_='posthead')
            if posthead:
                date_span = posthead.find('span', class_='postdate')
                if date_span:
                    date_text = date_span.get_text(strip=True)
                    post_data['date'] = self.parse_date(date_text)

                post_counter = posthead.find('a', class_='postcounter')
                if post_counter:
                    post_data['postlink'] = post_counter.get('href', '')

            # Extract title, images, and download links
            post_content = post_li.find('div', class_='postrow')
            if post_content:
                title_tag = post_content.find('h2', class_='title icon')
                title_text = title_tag.get_text(strip=True) if title_tag else ''
                post_data['title'] = title_text

                post_data['img_srcs'] = []
                post_data['img_files'] = []
                post_data['downloadlinks'] = []

                img_links = post_content.find_all('a', target='_blank')

                for link in img_links:
                    href = link.get('href', '')
                    img_tag = link.find('img')

                    is_image_host = any(domain in href for domain in self.img_hosts)
                    is_image_ext = href.endswith(self.img_ext)
                    has_img_inside = img_tag is not None

                    if is_image_host or is_image_ext or has_img_inside:
                        post_data['img_srcs'].append(href)

                        if img_tag:
                            img_src = img_tag.get('src', '')
                            if img_src:
                                post_data['img_files'].append(img_src)

                    is_file_host = any(host in href for host in self.file_hosts)
                    is_video_ext = href.endswith(self.vid_ext)
                    if is_file_host or is_video_ext:
                        post_data['downloadlinks'].append(href)

            return post_data

        except Exception as e:
            log("error", f"Error extracting post data: {e}")
            return None

    def find_posts(self, soup):
        """
        Find all posts from forum
        """
        try:
            postlist = soup.find('div', {'id': 'postlist'})
            if not postlist:
                log("warning", "No postlist found")
                return []

            posts_ol = postlist.find('ol', {'id': 'posts'})
            if not posts_ol:
                log("warning", "No posts ol found")
                return []

            posts = [
                li for li in posts_ol.find_all('li', class_='postbitlegacy')
                if not (li.get('id', '').startswith('post_thanks_box_'))
            ]

            log("info", f"Found {len(posts)} posts on this page")

            page_data = []
            for post in posts:
                post_data = self.extract_post_data(post)
                if post_data:
                    if self.forum_name:
                        post_data['forum_name'] = self.forum_name

                    if self.forum_link:
                        post_data['forum_link'] = self.forum_link

                    page_data.append(post_data)

            return page_data

        except Exception as e:
            log("error", f"Error finding posts: {e}")
            return []


def detect_os_arch():
    """
    Detect operating system architecture
    """
    system = platform.system().lower()
    machine = platform.machine().lower()

    if 'windows' in system:
        return 'win64' if '64' in machine else 'win32'
    elif 'darwin' in system:
        return 'mac-arm64' if 'arm' in machine or 'aarch64' in machine else 'mac-x64'
    elif 'linux' in system:
        return 'linux64'
    else:
        return None


def build_chromedriver_path(os_arch, headless=False):
    """
    Initialize chromedriver path
    """
    filename = 'chromedriver.exe' if 'win' in os_arch else 'chromedriver'
    driver_name = f'chromedriver-{os_arch}'
    if headless:
        filename = "chrome-headless-shell.exe" if 'win' in os_arch else 'chrome-headless-shell'
        driver_name = f'chrome-headless-shell-{os_arch}'

    return os.path.join('chromedrivers', driver_name, filename)


def ask_headless(arch, timeout=10):
    """
    Prompt the user whether to run in headless mode, with a timeout.
    Defaults to True (headless).
    """
    result = {"headless": True}
    
    if "linux" not in arch:
        def get_input():
            val = input("Would you like to run in headless mode? (y/N, default y): ").strip().lower()
            result["headless"] = val in ["y", '']

        thread = threading.Thread(target=get_input)
        thread.daemon = True
        thread.start()
        thread.join(timeout)

    return result["headless"]


def ask_disable_js(arch, timeout=10):
    """
    Prompt user to disable JavaScript, with timeout; defaults to True.
    """
    result = {"disable_js": True}

    if "linux" not in arch:
        def get_input():
            val = input("Disable JavaScript? (y/N, default y): ").strip().lower()
            result["disable_js"] = val in ['y', '']

        thread = threading.Thread(target=get_input, daemon=True)
        thread.start()
        thread.join(timeout)

    return result["disable_js"]


def create_driver(driverpath, disable_js, disable_images=True) -> webdriver.Chrome:
    """
    Create and configure a Chrome WebDriver instance.

    This function sets up a Selenium Chrome WebDriver with options and preferences
    defined. It allows enabling or disabling site permissions, JavaScript, image loading, and headless mode 
    based on the ChromeDriver path.

    Returns a configured Chrome WebDriver instance ready for automation.
    """
    options = Options()
    prefs = {}

    if disable_site_permissions:
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        prefs.update({
            "profile.default_content_setting_values.geolocation": 2,
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_setting_values.media_stream_mic": 2,
            "profile.default_content_setting_values.media_stream_camera": 2,
        })

    if disable_js:
        prefs["profile.managed_default_content_settings.javascript"] = 2

    if disable_images:
        prefs["profile.managed_default_content_settings.images"] = 2

    if prefs:
        options.add_experimental_option("prefs", prefs)

    if "chrome-headless-shell" in driverpath:
        standard_driver_path = build_chromedriver_path(os_arch, headless=False)
        options.binary_location = os.path.abspath(driverpath)
        service = Service(standard_driver_path)
    else:
        if "headless" in driverpath.lower():
            options.add_argument("--headless=new")
        service = Service(driverpath)

    return webdriver.Chrome(service=service, options=options)


def driver_config():
    os_arch = detect_os_arch()

    log("debug", f"OS: {os_arch}")
    time.sleep(2)

    headless = ask_headless(arch = os_arch)
    chromedriver_path = build_chromedriver_path(os_arch, headless) if os_arch else None
    time.sleep(1.5)

    log("debug", f"Chrome Driver: {chromedriver_path}")
    time.sleep(2)

    disable_js = ask_disable_js(arch=os_arch)

    if not os.path.isfile(chromedriver_path):
        raise FileNotFoundError(f"ChromeDriver not found at: {chromedriver_path}")

    return (os_arch, headless, disable_js, chromedriver_path)


def main():
    """
    Executes the primary workflow of the program.
    """
    arch, headless, load_js, driverpath = driver_config()

    driver = create_driver(driverpath=driverpath, disable_js=load_js)
    wait = WebDriverWait(driver, 10)
    log("info", f"{driver}")

    scraper = ForumScraper(driver, wait)
    
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
            log("error", f"Error in main driver quit: {last_err}")
            
        time.sleep(10)


if __name__ == '__main__':
    main()
