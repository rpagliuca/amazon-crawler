# Imports
import time
from selenium import webdriver
import selenium.webdriver.chrome.service as service
from selenium.webdriver.chrome.options import Options
import random
import pymongo
import sys

# Database
client = pymongo.MongoClient()
db = client.amazon
products = db.products


# Initialize webdriver
chrome_options = Options()
chrome_options.add_argument("--proxy-server=socks4://127.0.0.1:9050")
wd = webdriver.Chrome(chrome_options=chrome_options)

# Maximize window
wd.maximize_window()

# Start crawling

# Today's Deals
wd.get('https://www.amazon.com/gp/goldbox')

# Click on first deal and start from there
wd.find_element_by_css_selector('#widgetContent .a-row.layer.backGround').click()

# Now randomly browse related products and get their information
counter=0
while True:
    counter += 1

    try:
        # Get title of product
        title = wd.find_element_by_css_selector('#productTitle').text
        price = wd.find_element_by_css_selector('#price').text
        category = wd.find_element_by_css_selector('#wayfinding-breadcrumbs_feature_div').text
        rating = wd.find_element_by_css_selector('#averageCustomerReviews .a-icon-star').text
        url = wd.current_url

        # Insert into database
        product = {
            'title': title,
            'price': price,
            'category': category,
            'url': url,
            'rating': rating,
        }
        print product
        products.insert(product)
    except:
        print 'Caught exception. Skipping current product...'

    success = False 
    while not success:
        try:
            related_products = wd.find_elements_by_css_selector('#purchase-sims-feature a .a-section')
            product = random.choice(related_products)
            product.click()
            success = True
        except:
            print 'Caught exception. Retrying click on related product...'


# Close browser
wd.quit()
