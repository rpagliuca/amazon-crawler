# Imports
import time
from selenium import webdriver
import selenium.webdriver.chrome.service as service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import random
import pymongo
import sys
import pprint
import datetime

class AmazonCrawler:

    def init(self):
        # Database
        self.client = pymongo.MongoClient()
        self.db = self.client.amazon
        # Initialize webdriver
        chrome_options = Options()
        chrome_options.add_argument("--proxy-server=socks4://127.0.0.1:9050")
        self.wd = webdriver.Chrome(chrome_options=chrome_options)
        # Maximize window
        self.wd.maximize_window()

    def delete_cookies(self):
        self.wd.delete_all_cookies()

    def click_on_first_deal(self):
        # Today's Deals
        self.wd.get('https://www.amazon.com/gp/goldbox')
        # Click on first deal and start from there
        elements = self.wd.find_elements_by_xpath("//button[contains(text(), 'Add to Cart')]/ancestor::div[contains(@class, 'dealContainer')]/a[contains(@class, 'a-link-normal')]")
        first_deal = elements[0]
        ActionChains(self.wd).move_to_element(first_deal).click().perform()

    def click_on_random_related_product(self):
        time.sleep(1)
        related_products_group = self.wd.find_element_by_css_selector('#purchase-sims-feature')
        ActionChains(self.wd).move_to_element(related_products_group).perform()
        time.sleep(2) # Wait for ajax
        related_products = self.wd.find_elements_by_css_selector('#purchase-sims-feature a .a-section')
        product = random.choice(related_products)
        ActionChains(self.wd).move_to_element(product).click().perform()

    def get_product_details(self):
        # Get title of product
        title = self.wd.find_element_by_css_selector('#productTitle').text
        price = self.wd.find_element_by_css_selector('#price').text
        category = self.wd.find_element_by_css_selector('#wayfinding-breadcrumbs_feature_div').text
        rating = self.wd.find_element_by_css_selector('#averageCustomerReviews .a-icon-star span').get_attribute('textContent')
        url = self.wd.current_url
        product = {
            'title': title,
            'price': price,
            'category': category,
            'url': url,
            'rating': rating,
            'date': datetime.datetime.utcnow()
        }
        return product

    def store_product_details_on_db(self):
        product = self.get_product_details()
        self.db.products.insert(product)
        return product

    def print_and_store_product_details_on_db(self):
        product = self.store_product_details_on_db()
        print product

    def close(self):
        # Close browser
        self.wd.quit()

    def browse_to_last_product(self):
        last_product = self.db.products.find().sort([('_id', -1)]).limit(1)
        last_product = last_product[0]
        self.wd.get(last_product['url'])

ac = AmazonCrawler()

ac.init()
ac.delete_cookies()

# If we want to contitnue crawling...
ac.browse_to_last_product()

# If we want to restart fresh
# ac.click_on_first_deal()

def product_loop():
    try:
        while True:
            ac.print_and_store_product_details_on_db()
            ac.delete_cookies()
            ac.click_on_random_related_product()
    except:
        print "Caught exception. Browsing to last product URL..."
        ac.close()
        ac.init()
        ac.delete_cookies()
        ac.browse_to_last_product()
        product_loop()

product_loop()
