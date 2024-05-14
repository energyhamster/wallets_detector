import pytest
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Credentials for Dune Account
login = 'energy_hamster'
password = '4617aaeE5'


def login_to_dune(driver, login, password):
    driver.get('https://dune.com/browse/dashboards')
    driver.find_element(By.LINK_TEXT, 'Sign in').click()
    driver.find_element(By.NAME, 'username').send_keys(login)
    driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()


@pytest.fixture(scope="session")
def driver():
    options = Options()
    driver = uc.Chrome()
    driver.implicitly_wait(160)
    options.add_argument("--window-size=1920,1080")

    login_to_dune(driver, login, password)

    try:
        yield driver
    finally:
        driver.quit()
