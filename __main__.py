import time

from selenium import webdriver
import selenium.webdriver.chrome.service as service

service = service.Service('chromedriver')
service.start()
capabilities = {}
wd = webdriver.Remote(service.service_url, capabilities)
wd.maximize_window()
wd.get('http://alinerafa.com.br')
wd.find_element_by_id('senha_acesso').send_keys('convidado especial')
wd.find_element_by_css_selector('button').click()
wd.find_element_by_id('menu-item-241').click()
print wd.find_element_by_css_selector('.site-main span').text
wd.quit()
