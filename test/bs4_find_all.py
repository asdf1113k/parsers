import requests
from bs4 import BeautifulSoup


response = requests.get("https://google.com")

soup = BeautifulSoup(response.text, "lxml")
for tag in soup.find_all():
    print(tag.get("href"))


# я узнал что find_all без параметров возвращает <class 'bs4.element.ResultSet'>
# а из <class 'bs4.element.ResultSet'> берутся <class 'bs4.element.Tag'>


all_tags = soup.find()
# выводят одно и тоже
print(all_tags)
print(response.text)
# просто разные объекты
print(type(all_tags))  # <class 'bs4.element.ResultSet'>
print(
    type(response.text)
)  # <class 'requests.models.Response'> c методом text <class 'str'>


# что я узанл с этого
