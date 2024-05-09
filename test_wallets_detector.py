import os
import logging
import telebot
import time
# import pyautogui as pg
from contextlib import contextmanager
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException

# Configure logging to capture key events and errors
logging.basicConfig(
    filename='token_activity.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Credentials for Dune Account
login = 'energy_hamster'
password = '4617aaeE5'

# Telegram bot ID's
bot_token = '5571166427:AAHmG8cSK4MLtbhvrDLjT3qo3UpGGfhsIKA'
chat_id = '-1001915065412'

bot = telebot.TeleBot(bot_token)


def send_telegram_message(message_text):
    bot.send_message(chat_id, message_text, parse_mode='html')


@contextmanager
def get_driver(options):
    driver = uc.Chrome(options=options)
    try:
        yield driver
    finally:
        driver.quit()


def login_to_dune(driver, login, password):
    driver.get('https://dune.com/browse/dashboards')
    driver.find_element(By.LINK_TEXT, 'Sign in').click()
    driver.find_element(By.NAME, 'username').send_keys(login)
    driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()


wallet_counter = 1


def test_check_token_wallets(driver, token):
    global today_wallet_created, yesterday_wallet_created, wallet_counter
    try:
        driver.get(
            f'https://dune.com/queries/1897591/3123566?chain_e15077=ethereum&day_n26d66=15&token_address_t6c1ea={token}')
        time.sleep(1)
        driver.find_element(By.ID, 'run-query-button').click()
        time.sleep(1)
        driver.find_element(By.XPATH, "//button[contains(text(),'Cancel')]")
        time.sleep(1)

        today_wallet_created = driver.find_element(By.CSS_SELECTOR, 'tbody tr:nth-child(1) td:nth-child(1)').text
        yesterday_wallet_created = driver.find_element(By.CSS_SELECTOR, 'tbody tr:nth-child(2) td:nth-child(1)').text

        difference = int(today_wallet_created) - int(yesterday_wallet_created)
        logging.info(f"Token: {token}, Wallet Difference: {difference}")

        #wallet_created_raise = int(today_wallet_created) > int(yesterday_wallet_created) * 2
        wallet_created_raise = True

        #if wallet_created_raise and difference >= 100:
        if wallet_created_raise:
            logging.info(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! BUY ALERT for Token: {token}")
            logging.info(f"Difference: {difference}")
            logging.info(f"Today wallets created: {today_wallet_created}")
            logging.info(f"Yesterday wallets created: {yesterday_wallet_created}")

            send_telegram_message(f"BUY ALERT for Token: {token}\n"
                                  f"Difference: {difference}\n"
                                  f"Today wallets created: {today_wallet_created}\n"
                                  f"Yesterday wallets created: {yesterday_wallet_created}\n")
        else:
            logging.info(f"Token {token} does not meet the criteria")
        time.sleep(1)
        print(wallet_counter)
        wallet_counter += 1
        # pg.click(495, 468)

    except TimeoutException as e:
        logging.error(f"Timeout for token {token}: {e}")
    except WebDriverException as e:
        logging.error(f"WebDriver error for token {token}: {e}")
    except Exception as e:
        logging.error(f"Unexpected error for token {token}: {e}")


# Main execution with context manager for safety and clean shutdown
opts = uc.ChromeOptions()
# uc.TARGET_VERSION = 85  # This is the targeted Chrome version
with get_driver(opts) as driver:
    driver.implicitly_wait(160)
    opts.add_argument("--window-size=1900,2000")
    login_to_dune(driver, login, password)

    with open('tokens_test.txt', 'r') as file:
        token_list = file.readlines()
        for token in token_list:
            token = token.strip()
            check_token_wallets(driver, token)

    time.sleep(3)
