import pytest
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


@pytest.fixture()
def driver():
    options = Options()
    driver = uc.Chrome()
    driver.implicitly_wait(160)
    options.add_argument("--window-size=1920,1080")
    try:
        yield driver
    finally:
        driver.quit()
