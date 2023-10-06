from pymongo import MongoClient
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import quote


client = MongoClient("mongodb://localhost:27017/")
db = client["data_shopee"]
collection = db["products"]

# Setting browser selenium
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(options=options)

start = 0
count_mor = 0

while True:
    result = collection.find({}).skip(start).limit(10000)
    stop_w = 0
    for k, i in enumerate(list(result)):
        count_mor += 1
        stop_w += k
        url = quote(i['product_url'].split('https://')[1])
        print('https://' + url)
        browser.get('https://' + url)

        time.sleep(3)
        elements = browser.find_element(By.CLASS_NAME, "_1k47d8")
        print(elements.text)
        break
    break
    # if stop_w == 0:
    #     break
    start += 10000