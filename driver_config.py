import os
import platform
import threading
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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


def ask_headless(timeout=10):
    """
    Prompt the user whether to run in headless mode, with a timeout.
    Defaults to True (headless).
    """
    result = {"headless": True}

    def get_input():
        val = input("Would you like to run in headless mode? (y/N, default y): ").strip().lower()
        result["headless"] = val in ["y", '']

    thread = threading.Thread(target=get_input)
    thread.daemon = True
    thread.start()
    thread.join(timeout)
    return result["headless"]


def ask_disable_js(timeout=10):
    """
    Prompt user to disable JavaScript, with timeout; defaults to True.
    """
    result = {"disable_js": True}

    def get_input():
        val = input("Disable JavaScript? (y/N, default y): ").strip().lower()
        result["disable_js"] = val in ['y', '']

    thread = threading.Thread(target=get_input, daemon=True)
    thread.start()
    thread.join(timeout)
    return result["disable_js"]


def create_driver() -> webdriver.Chrome:
    """
    Create and configure a Chrome WebDriver instance.

    This function sets up a Selenium Chrome WebDriver with options and preferences
    defined. It allows enabling or disabling site permissions, JavaScript, and headless mode 
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

    if prefs:
        options.add_experimental_option("prefs", prefs)

    if "chrome-headless-shell" in chromedriver_path:
        standard_driver_path = build_chromedriver_path(os_arch, headless=False)
        options.binary_location = os.path.abspath(chromedriver_path)
        service = Service(standard_driver_path)
    else:
        if "headless" in chromedriver_path.lower():
            options.add_argument("--headless=new")
        service = Service(chromedriver_path)

    return webdriver.Chrome(service=service, options=options)


disable_site_permissions = True
os_arch = detect_os_arch()
print(f"OS: {os_arch}")
time.sleep(2)
headless = ask_headless()
chromedriver_path = build_chromedriver_path(os_arch, headless) if os_arch else None
time.sleep(1.5)
print(f"Chrome Driver: {chromedriver_path}")
time.sleep(2)
disable_js = ask_disable_js()

if not os.path.isfile(chromedriver_path):
    raise FileNotFoundError(f"ChromeDriver not found at: {chromedriver_path}")

driver = create_driver()