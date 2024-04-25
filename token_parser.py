import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

uc.TARGET_VERSION = 85
opts = uc.ChromeOptions()
driver = uc.Chrome(options=opts)
driver.implicitly_wait(20)

x = 26

try:
    while x != 0:
        driver.get('https://etherscan.io/tokens?p=26')
        token = driver.find_element(By.XPATH,
                                    f'//body[1]/main[1]/section[2]/div[1]/div[2]/div[1]/table[1]/tbody[1]/tr[{x}]/td[2]/a[1]/img[1]')
        token2 = driver.find_element(By.XPATH,
                                     f'//body[1]/main[1]/section[2]/div[1]/div[2]/div[1]/table[1]/tbody[1]/tr[{x - 2}]/td[2]/a[1]/img[1]')
        actions = ActionChains(driver)
        actions.move_to_element(token).perform()

        time.sleep(1)
        token2.click()
        token_number = driver.find_element(By.CSS_SELECTOR, '.text-truncate.d-block')
        print(token_number.text)
        x -= 1

        time.sleep(3)

except OSError as e:
    print("An error occurred:", e)
except Exception as e:
    print("An error occurred:", e)

finally:
    driver.quit()
