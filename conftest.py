import pytest
import undetected_chromedriver as uc


@pytest.fixture()
def driver():
    driver = uc.Chrome()
    driver.implicitly_wait(160)
    driver.maximize_window()
    try:
        yield driver
    finally:
        driver.quit()