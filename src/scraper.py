import os
import logging
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# TODO: Add logging INFO messages for each stage


def scraper_init() -> WebDriver:
    """
    Initialises selenium
    """
    # driver = webdriver.Firefox()

    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    return driver


def navigator(driver: WebDriver, url: str) -> None:
    """
    Connects to a given url
    """
    print(f"Starting connecting to {url}")
    driver.get(url)
    sleep(3)


def cookie_handler(driver: WebDriver) -> None:
    """
    Rejects cookies for the DR page
    """

    wait = WebDriverWait(driver, 10)

    wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div[1]/div/div/div/div/div/div/div/div/div/div/div[3]/div/div[2]/button",
            )
        )
    ).click()

    sleep(2)


def button_clicker(driver: WebDriver, button_name: str) -> None:
    """
    Clicks on button tabs within page to generate dynamic content in the page
    """

    element = driver.find_element(By.XPATH, f'//button[text()="{button_name}"]')
    # elements = driver.find_elements(By.XPATH, '//button[text()="2023"]') #make later part an fstring that connects to the year global VAR
    try:
        element.click()
    except Exception as e:
        print(f"Element not found: {e}, check the XPATH or the list of button_names")


def clicker_scroller(driver: WebDriver) -> None:
    """
    Clicks on "Vis Flere" on the DR page, it also scrolls if necessary
    """
    while True:
        try:
            vis_flere_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "/html/body/div/div[1]/main/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div[2]/button",
                    )
                )
            )

            vis_flere_button.click()

        except (TimeoutException, NoSuchElementException):
            break


def html_writer(driver: WebDriver, output_folder: str, file_name: str) -> None:
    """
    Saves the 'complete' HTML to the output html folder
    """
    page_html = driver.page_source
    print(page_html)

    file_path = os.path.join(output_folder, f"html_{file_name}.html")

    with open(file_path, "w", encoding="utf-8") as file:  # also make it into a fstring
        file.write(page_html)

    print(f"HTML content saved to {file_path}")
