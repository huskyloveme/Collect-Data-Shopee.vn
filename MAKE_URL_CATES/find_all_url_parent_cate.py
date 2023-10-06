import time
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(options=options)

browser.get('https://shopee.vn/')
time.sleep(3)
elements = browser.find_elements(By.CLASS_NAME, "image-carousel__item")

for i in elements:
    a_element = i.find_element(By.TAG_NAME,'a')
    url = a_element.get_attribute('href')
    with open('list_parent_categories.txt', 'a') as file:
        file.write(str(url).strip(''))
        file.write('\n')

browser.quit()