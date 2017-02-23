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
    pprint.pprint(product['title'])
    print "============================"
