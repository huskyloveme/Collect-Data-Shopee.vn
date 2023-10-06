Project description:
- Collect and handle data from shopee e-commerce
- Take about 3k products from big categories

![img.png](img.png)

- Collect data flow:

    + Step1: Take all the big categories on Shopee:
  
        + run file _**find_all_url_parent_cate.py**_ -> list_parent_categories.txt

    + Step2: Take all the children categories of big categories: 
  
        + run file **_find_all_url_parent_cate.py__** -> list_parent_categories.txt
      
    + Step3: Take all product on 9 pages on each url children categories:

        + run _**main.py**_ -> MongoDB -> **_extract.py_** -> product.csv
        RESULT: about ~ 120k products

    + Step4: Load data from MongoDB to CSV
        + run mongo_to_csv.py -> data_products.csv
