# парсер ссылок с домена wwwww.jodi.org

import requests as rq
from bs4 import BeautifulSoup

domain = "https://wwwww.jodi.org/"


class ParserLinks:
    def __init__(self, url: str):
        self.links:list = []
        self.used_links = set()
        self.url :str   = url
        self.html:str   = self.get_html(url)

    def get_html(self, url, plus_url=""):
        if f'{url}{plus_url}' in self.used_links:
            return "<html> </html>"
            

        if rq.get(f'{url}{plus_url}').text == 200:
            self.used_links.add(f'{self.url}{plus_url}')
            return rq.get(f'{url}{plus_url}').text
        else:
            return "<html> </html>"

    def search_links(self):
        soup = BeautifulSoup(self.html, "lxml")

        tags_a = soup.find_all("a")
        for tag_a in tags_a:
            self.links.append(tag_a.get("href"))

    def run(self):
        self.search_links()

        while len(self.links) > 0:
            self.html = self.get_html(self.url, self.links[0])
            self.links.pop(0)
            self.search_links()
            print(f'спарсено ссылок: {len(self.used_links)}')
            print(f'спарсеные ссылки: {self.used_links}')



if __name__ == "__main__":
    parser = ParserLinks(domain)
    parser.run()
    print(parser.url)
    print(parser.links)
    print(parser.used_links)


    # мой старый код
    # links = Links()
    # controller(domain)

    # код мена с чата
    # controller_class = Controller([domain])
    # controller.run()
