from dataclasses import dataclass
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from urllib.parse import urljoin
import pandas as pd


BASE_URL = "https://webscraper.io/"
HOME_URL = urljoin(BASE_URL, "test-sites/e-commerce/more/")


@dataclass
class Product:
    title: str
    description: str
    price: float
    rating: int
    num_of_reviews: int


def get_driver() -> WebDriver:
    options = Options()
    options.headless = True
    service = Service(executable_path="C:/chromedriver-win64/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def scrape_page(driver: WebDriver, url: str) -> list[Product]:
    driver.get(url)
    products = []

    while True:
        try:
            more_button = driver.find_element(By.CLASS_NAME, "btn.btn-primary")
            driver.execute_script("arguments[0].click();", more_button)

            if "display: none" in more_button.get_attribute("style"):
                break
        except NoSuchElementException:
            break

    product_elements = driver.find_elements(By.CLASS_NAME, "thumbnail")
    for product_element in product_elements:
        title = product_element.find_element(
            By.CLASS_NAME, "title").get_attribute("title")
        description = product_element.find_element(
            By.CLASS_NAME, "description").text
        price = float(product_element.find_element(
            By.CLASS_NAME, "price").text.replace("$", ""))
        rating = len(product_element.find_elements(
            By.CLASS_NAME, "ws-icon-star"))
        num_of_reviews = int(product_element.find_element(
            By.CLASS_NAME, "ratings").text.split()[0])

        product = Product(title, description, price, rating, num_of_reviews)
        products.append(product)

    return products


def save_products_to_csv(products: list[Product], filename: str) -> None:
    product_data = {
        "title": [p.title for p in products],
        "description": [p.description for p in products],
        "price": [p.price for p in products],
        "rating": [p.rating for p in products],
        "num_of_reviews": [p.num_of_reviews for p in products],
    }

    df = pd.DataFrame(product_data)
    df.to_csv(filename, index=False)


def get_all_products() -> None:
    driver = get_driver()

    try:
        home_products = scrape_page(driver, HOME_URL)
        save_products_to_csv(home_products, "home.csv")

        computers_url = urljoin(BASE_URL,
                                "test-sites/e-commerce/more/computers")
        computer_products = scrape_page(driver, computers_url)
        save_products_to_csv(computer_products, "computers.csv")

        laptops_url = urljoin(BASE_URL,
                              "test-sites/e-commerce/more/computers/laptops")
        laptops_products = scrape_page(driver, laptops_url)
        save_products_to_csv(laptops_products, "laptops.csv")

        tablets_url = urljoin(BASE_URL,
                              "test-sites/e-commerce/more/computers/tablets")
        tablets_products = scrape_page(driver, tablets_url)
        save_products_to_csv(tablets_products, "tablets.csv")

        phones_url = urljoin(BASE_URL,
                             "test-sites/e-commerce/more/phones")
        phones_products = scrape_page(driver, phones_url)
        save_products_to_csv(phones_products, "phones.csv")

        touch_url = urljoin(BASE_URL,
                            "test-sites/e-commerce/more/phones/touch")
        touch_products = scrape_page(driver, touch_url)
        save_products_to_csv(touch_products, "touch.csv")

    finally:
        driver.quit()


if __name__ == "__main__":
    get_all_products()
