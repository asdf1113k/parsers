# парсер ссылок с домена wwwww.jodi.org

import requests as rq
from bs4 import BeautifulSoup

domain = "https://wwwww.jodi.org/"


class Controller:
    def __init__(self, urls: list):
        self.queue_links: list = urls
        self.visited_links = set()

    def run(self):
        while len(self.queue_links) > 0:
            current_link = self.queue_links.pop(0)
            if current_link in self.visited_links:
                continue
            self.visited_links.add(current_link)

    def search_links(self, url):
        soup = BeautifulSoup(rq.get(url).text, "lxml")
        for tag_a in soup.find_all("a"):
            self.queue_links.append(tag_a)


class Links:
    def __init__(self):
        self.links = []
        self.used_links = set()

    def get(self) -> set:
        return set(self.links)

    def add(self, link):
        self.links.append(link)


def get_html(domain, path_url=""):
    responce = rq.get(domain + path_url)
    return responce.text


def searching_links_and_add(html):
    soup = BeautifulSoup(html, "lxml")
    tags_a = soup.find_all("a")
    for a in tags_a:
        links.add(a.get("href"))



def write_links_in_file(): ...


def controller(url) -> None:
    searching_links_and_add(get_html(url))
    while len(links.get()) > 0:
        break
    for n in range(10):
        print(links.get())
        print(f"отрработало {n} раз")
        for path in links.get():
            searching_links_and_add(get_html(url, path_url=path))
    else:
        print(links.get())


if __name__ == "__main__":
    links = Links()
    controller(domain)

    # код мена с чата
    # controller_class = Controller([domain])
    # controller.run()
