import time
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(options=options)

file_name = 'list_child_categories.txt'

def take_url(url_parent_cate, file_name):
    element = []

    browser.get(url_parent_cate)
    time.sleep(3)

    browser.execute_script(f"window.scrollTo(0, 1600);")
    time.sleep(3)

    element = browser.find_element(By.CLASS_NAME, "shopee-category-list__sub-category-list")

    list_a_tag_child_cate = element.find_elements(By.TAG_NAME,'a')
    print("Count children cates: " + str(len(list_a_tag_child_cate)) + " of BIG CATE: " + url_parent_cate)
    for child_cate in list_a_tag_child_cate:
        url = child_cate.get_attribute('href')
        with open(file_name, 'a') as file:
            file.write(str(url))
            file.write('\n')

with open('list_parent_categories.txt', 'r') as file:
    for index, line in enumerate(file):
        if "http" in str(line):
            take_url(str(line).strip('\n'), file_name)
            print(f"Done - {line}")

browser.quit()