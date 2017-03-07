# Imports
import time
import random
import pymongo
import sys
import pprint

# Database
client = pymongo.MongoClient()
db = client.amazon

for product in db.products.find():
    print("Title: " + product['title'])
    print("Price: " + product['price'].replace('\n', '; '))
    print("Category: " + product['category'].replace('\n', ' '))
    print("URL: " + product['url'])
    print("Rating: " + product['rating'])
    print "============================"
