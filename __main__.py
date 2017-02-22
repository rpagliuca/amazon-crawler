# Imports
import time
from selenium import webdriver
import selenium.webdriver.chrome.service as service
from selenium.webdriver.chrome.options import Options

# Teste com Chrome Driver
chrome_options = Options()
chrome_options.add_argument("--proxy-server=socks4://127.0.0.1:9050")
wd = webdriver.Chrome(chrome_options=chrome_options)

# Teste com Remote Driver
#service = service.Service('chromedriver')
#service.start()
#wd = webdriver.Remote(service.service_url, capabilities)

# Manipular driver
wd.maximize_window()

# Start crawling

# Today's Deals
wd.get('https://www.amazon.com/gp/goldbox')

# Click on first deal and start from there
wd.find_element_by_css_selector('#widgetContent .a-row.layer.backGround').click()

# Gets information from current product

# Now randomly browse related products and gets their information

# Waits
time.sleep(5)

# Close browser
wd.quit()
