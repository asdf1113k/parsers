# парсер с рекурсивным парсингом ссылок и без него V2

from requests import get

from bs4 import BeautifulSoup

class Parser:
    def __init__(self, url, recursion_search: bool=False):
        self.url = url
        self.html = ""
        self.links = []
        self.cheaking_links = set()
        self.count_recursion = 300
        self.count_get_html = 0
    
    def get_html(self, url):
        self.count_get_html += 1
    
        response = get(url)
        if 200< response.status_code < 399:
            if url not in self.cheaking_links:
                self.html = response.text
                self.cheaking_links.add(response.url)
            else:
                self.html = "<html></html>"
                return

    def search_links(self):
        soup = BeautifulSoup(self.html, "lxml")
        for tag in soup.find_all():
            if tag.get("href") is None:
                continue
            if f"{self.url}{tag.get('href')}" not in self.cheaking_links:
                self.links.append(f"{self.url}{tag.get('href')}")

                
    
    def run(self):
        self.get_html(self.url)
        self.search_links()
        # while len(self.links) > 0:
            # recursion_links = self.links
            # for link in recursion_links:
                

            
if __name__ == "__main__":
    ...
 


        