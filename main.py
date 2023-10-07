import time
from schema import schema_data
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from mongo_to_csv import collection

current_directory = os.path.dirname(os.path.abspath(__file__))

def list_url_cates():
    list_urls = []
    file_path = os.path.join(current_directory, 'MAKE_URL_CATES/list_child_categories.txt')
    with open(file_path, "r") as file:
        for line in file:
            if str(line).strip("\n") != "":
                list_urls.append(str(line).strip("\n"))
    return list_urls

if __name__ == '__main__':

    # Setting browser selenium
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(options=options)

    # Get URL each cates
    for ind, url in enumerate(list_url_cates()):
        count_collected = 0
        count_real = 0
        for page in range(9):
            browser.get(url + f"?page={page}")
            time.sleep(3)
            elements = browser.find_elements(By.CLASS_NAME, "shopee-search-item-result__item")
            browser.execute_script(f"window.scrollTo(200, {800});")
            count_real += len(elements)
            data_product = schema_data
            for index, element in enumerate(elements):
                if element.text:
                    try:
                        count_collected += 1
                        # Handle each field data
                        a_element = element.find_element(By.TAG_NAME, 'a')
                        if a_element:
                            # URL
                            data_product['product_url'] = a_element.get_attribute('href').split("?sp_atk=")[0]

                            # NAME
                            name_element = a_element.find_element(By.CLASS_NAME, 'APSFjk')
                            if name_element:
                                data_product['product_name'] = name_element.text

                            # PRICE
                            price = None
                            price_element = a_element.find_elements(By.CLASS_NAME, 'KwA6xi')
                            if price_element:
                                if len(price_element) > 1:
                                    data_product['product_price'] = price_element[0].text + ' - ' + price_element[1].text
                                    price = (int(price_element[0].text.replace('.','')) + int(price_element[1].text.replace('.','')))/2
                                else:
                                    data_product['product_price'] = price_element[0].text
                                    price = int(price_element[0].text.replace('.',''))

                            # SOLD OUT
                            sold_out_element = a_element.find_element(By.CLASS_NAME, 'QE5lnM')
                            if sold_out_element:
                                sold_out_string = sold_out_element.text
                                sold_out_string = sold_out_string.replace("Đã bán ", "")
                                if "," in sold_out_string:
                                    sold_out_string = sold_out_string.replace("k", "00")
                                    sold_out_string = sold_out_string.replace(",", "")
                                else:
                                    sold_out_string = sold_out_string.replace("k", "000")
                                data_product['product_soldout'] = int(sold_out_string)

                            # REVENUE
                            if data_product['product_soldout'] and price:
                                data_product['product_revenue'] = price * data_product['product_soldout']

                            # RATING
                            list_rating = a_element.find_elements(By.CLASS_NAME,"shopee-rating-stars__lit")
                            if list_rating:
                                rating = 0
                                for rat in list_rating:
                                    str_rating = str(rat.get_attribute('style')).strip('%;').split('width: ')[1]
                                    float_rating = float(str_rating)/100
                                    rating += float_rating
                                data_product['product_rating'] = round(rating,1)
                            document = data_product.copy()
                            x = collection.insert_one(document)
                    except Exception as e:
                        continue

                if index % 4 == 0:
                    browser.execute_script(f"window.scrollTo(200, {800+320*(index/4)});")

        with open("LOG/log_crawl.txt", "a") as file_log:
            file_log.write(f"CATE: {ind}, with {count_collected}/{count_real} products\n")


        print(f"CATE: {ind}, with {count_collected}/{count_real} products")

