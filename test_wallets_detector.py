import os
import logging
import telebot
import time
import pytest
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

# Telegram bot ID's
bot_token = '5571166427:AAHmG8cSK4MLtbhvrDLjT3qo3UpGGfhsIKA'
# chat_id = '-1001915065412'
chat_id = '-1002135761277'

bot = telebot.TeleBot(bot_token)


def send_telegram_message(message_text):
    bot.send_message(chat_id, message_text, parse_mode='html')


wallet_counter = 1


def check_token_wallets(driver, token, exchange):
    global today_wallet_created, yesterday_wallet_created, wallet_counter
    try:
        driver.get(
            f'https://dune.com/queries/1897591/3123566?chain_e15077=ethereum&day_n26d66=2&token_address_t6c1ea={token}')
        time.sleep(1)
        driver.find_element(By.ID, 'run-query-button').click()
        time.sleep(1)
        driver.find_element(By.XPATH, "//button[contains(text(),'Cancel')]")
        time.sleep(1)

        today_wallet_created = driver.find_element(By.CSS_SELECTOR, 'tbody tr:nth-child(1) td:nth-child(1)').text
        yesterday_wallet_created = driver.find_element(By.CSS_SELECTOR, 'tbody tr:nth-child(2) td:nth-child(1)').text

        difference = int(today_wallet_created) - int(yesterday_wallet_created)
        logging.info(f"Token: {token}, Wallet Difference: {difference}")

        wallet_created_raise = int(today_wallet_created) > int(yesterday_wallet_created) * 2

        if wallet_created_raise and difference >= 100:
            logging.info(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! BUY ALERT for Token on {exchange}: {token}")
            logging.info(f"Difference: {difference}")
            logging.info(f"Today wallets created: {today_wallet_created}")
            logging.info(f"Yesterday wallets created: {yesterday_wallet_created}")

            send_telegram_message(
                f"BUY SIGNAL ALERT for Token on {exchange}: https://dexscreener.com/ethereum/{token}\n"
                f"Difference: {difference}\n"
                f"Today wallets created: {today_wallet_created}\n"
                f"Yesterday wallets created: {yesterday_wallet_created}\n")
        else:
            logging.info(f"Token {token} does not meet the criteria on {exchange}")
        time.sleep(1)
        print(wallet_counter)
        wallet_counter += 1
        # pg.click(495, 468)

    except TimeoutException as e:
        logging.error(f"Timeout for token {token} on {exchange}: {e}")
    except WebDriverException as e:
        logging.error(f"WebDriver error for token {token} on {exchange}: {e}")
    except Exception as e:
        logging.error(f"Unexpected error for token {token} on {exchange}: {e}")


def read_tokens_from_file(file_path):
    with open(file_path, 'r') as file:
        tokens = [line.strip() for line in file if line.strip()]
    return tokens


@pytest.mark.parametrize("token", read_tokens_from_file('binance.txt'))
def test_get_wallets_for_binance(driver, token):
    check_token_wallets(driver, token, exchange="Binance")
    time.sleep(1)
