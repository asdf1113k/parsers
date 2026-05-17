from time import sleep

import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

options = Options()
options.add_argument("--headless")  # без GUI
driver = webdriver.Chrome(options=options)

driver.get("https://stepik.org/catalog")
sleep(10)
html = driver.page_source  # уже с выполненным JS
driver.quit()


html = BeautifulSoup(html, "lxml")

names_classes = []
count = 0
for tag in html.find_all():
    count += 1
    names_classes.append(tag.get("class"))
else:
    print(count)


# print(set(names_classes)) # так нельзя сделать так как names_classes obj 'bs4.element.AttributeValueList'
names_classes = str(names_classes)
names_classes = names_classes.replace("[", "")
names_classes = names_classes.replace("]", "")
names_classes = names_classes.replace("'", "")


print(set(names_classes.split(", ")))
