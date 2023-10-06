import json

from pymongo import MongoClient
import csv
from schema import schema_data
client = MongoClient("mongodb://localhost:27017/")
db = client["data_shopee"]
collection = db["products"]

#Write header CSV
with open('output_data.csv', 'w',newline='') as csvfile:
    csvfile = csv.DictWriter(csvfile, fieldnames=['name', 'product_URL', 'rating', 'price', 'sold_out', 'revenue'])
    csvfile.writeheader()

#Write data CSV
start = 0
count_mor = 0
try:
    while True:
        result = collection.find({}).skip(start).limit(10000)
        stop_w = 0
        for k, i in enumerate(list(result)):
            count_mor += 1
            stop_w += k
            del i['_id']
            with open('output_data.csv', 'a', encoding='utf-8', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([
                    i['product_name'],
                    i['product_url'],
                    i['product_rating'],
                    i['product_price'],
                    i['product_soldout'],
                    i['product_revenue'],
                ])
        if stop_w == 0:
            break
        start += 10000
    print("Created file successfully!")
except:
    print("Created file failed!")