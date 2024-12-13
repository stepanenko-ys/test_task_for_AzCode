from datetime import datetime
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver as base_webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from seleniumwire import webdriver as webdriver_with_proxy
from selenium.webdriver.support import expected_conditions as EC

import os

def setup_webdriver(headless: bool, proxy: dict = None):
    options = base_webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')

    if headless:
        options.add_argument("--headless")

    if proxy:
        # If requests require using proxy servers that need authentication,
        # it is recommended to use selenium-wire instead of regular selenium.
        # This is because selenium-wire provides built-in support for handling
        # authenticated proxies.
        driver = webdriver_with_proxy.Chrome(
            service=Service(ChromeDriverManager().install()),
            seleniumwire_options={'proxy': proxy},
            options=options
        )
        return driver

    driver = base_webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    return driver

def check_dir_existence(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def generate_filename():
    return datetime.now().strftime("%Y-%m-%d__%H-%M-%S")

def get_login_form(url: str, headless: bool):
    driver = setup_webdriver(headless=headless)
    try:
        driver.get(url)
        WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "login-form")
            )
        )

        login_form = driver.find_element(By.CLASS_NAME, "login-form")
        if login_form:
            check_dir_existence("login_forms")
            file_path = f"login_forms/{generate_filename()}.html"

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(login_form.get_attribute("outerHTML"))
        else:
            print("No login form found on the page.")
    except Exception as e:
        print(f"Error fetching login form: {e}")
    finally:
        driver.quit()

def get_promotions(url: str, headless: bool, proxy: dict):
    driver = setup_webdriver(headless=headless, proxy=proxy)
    try:
        driver.get(url)
        WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "promotions-single")
            )
        )
        soup = BeautifulSoup(driver.page_source, "html.parser")

        promotions = soup.find_all(class_="promotions-single")
        if promotions:
            check_dir_existence("promotions")
            file_path = f"promotions/{generate_filename()}.csv"

            with open(file_path, "w", encoding="utf-8") as f:
                for promo in promotions:
                    promo_title = promo.find(class_="promotions-single__title")
                    promo_txt = promo.find(class_="promotions-single__txt")
                    promo_link = promo.find(class_="promotions-single__btn-wrap").find("a")

                    f.write(
                        f"{promo_title.get_text(strip=True)};"
                        f"{promo_txt.get_text(strip=True)};"
                        f"{promo_link.get('href')}\n"
                    )
        else:
            print("No promotions found on the page.")
    except Exception as e:
        print(f"Error fetching promotions: {e}")
    finally:
        driver.quit()

def get_bonuses(url: str, headless: bool):
    driver = setup_webdriver(headless=headless)
    try:
        driver.get(url)
        WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "bonuses-app-list__item")
            )
        )
        soup = BeautifulSoup(driver.page_source, "html.parser")

        bonuses = soup.find_all(class_="bonuses-app-list__item")
        if bonuses:
            check_dir_existence("bonuses")
            file_path = f"bonuses/{generate_filename()}.csv"
            with open(file_path, "w", encoding="utf-8") as f:
                for bonus in bonuses:
                    bonus_name = bonus.find(class_="bonuses-bonus-tile-name__compile")
                    bonus_link = bonus.find("a", class_='bonuses-app-list__block')

                    f.write(
                        f"{bonus_name.get_text(strip=True)};"
                        f"{bonus_link.get('href')}\n"
                    )
        else:
            print("No bonuses found on the page.")
    except Exception as e:
        print(f"Error fetching bonuses: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    headless_mode = False

    proxy_server = {
        'https': 'https://brd-customer-hl_e81f440b-zone-isp_proxy1:0dtl53ky3y24@brd.superproxy.io:33335'
    }

    login_form_url = "https://go.slotimo.com/login/"
    get_login_form(login_form_url, headless_mode)

    promotions_url = "https://www.woocasino.com/promotions"
    get_promotions(promotions_url, headless_mode, proxy_server)

    bonuses_url = "https://betandyou-227625.top/pl/bonus/rules"
    get_bonuses(bonuses_url, headless_mode)
