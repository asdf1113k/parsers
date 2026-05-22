# парсер с рекурсивным парсингом ссылок и без него V2

from requests import Response, get

from bs4 import BeautifulSoup

class Parser:
    def __init__(self, url, recursion_search: bool=False, auto_run=False) -> None:
        self.url: str = self.set_url(url)
        self.html: str = ""
        self.links = []
        self.cheaking_links = set()
        self.count_recursion = 300
        self.count_get_html = 0

        if auto_run:
            self.run()
    
    def set_url(self, new_url:str) -> str:
        if new_url.startswith("https://", 0, 8) and new_url[-1] == "/":
            return new_url
        else: 
            raise ValueError(f"переданный url({new_url}) не соответствует качествам url. пример как должен выглядеть url (https://google.com/)")
            
    def set_auto_run(self, new_value:bool) -> None:
        if type(new_value) is bool:
            self.auto_run = new_value
        else:
            raise ValueError(f"в {self.set_auto_run.__name__} передано не bool значение")

    def get_html(self, url) -> None:
        self.count_get_html += 1
    
        response: Response = get(url)
        if 200 <= response.status_code <= 399:
            if url not in self.cheaking_links:
                self.html: str = response.text
                self.cheaking_links.add(response.url)
                return
        else:
            self.html = "<html></html>"
            return

    def search_links(self) -> None:
        soup = BeautifulSoup(self.html, "lxml")
        for tag in soup.find_all():
            if tag.get("href") is None:
                continue
            if f"{self.url}{tag.get('href')}" not in self.cheaking_links:
                self.links.append(f"{self.url}{tag.get('href')}")

                
    
    def run(self) -> None:
        self.get_html(self.url)
        self.search_links()
        while len(self.links) > 0:
            print(f"запросов сделано            : {self.count_get_html}")
            print(f"ссылок на очередь парсинга  : {len(self.links)}")
            print(f"спарсеные ссылки            : {len(self.cheaking_links)}")
            print(f"links :{self.links}")
 
            recursion_links = self.links
            for link in recursion_links:
                self.get_html(link)
                self.search_links

                

            
if __name__ == "__main__":
    url = "https://wwwww.jodi.org/"
    parser = Parser(url, auto_run=True)
    print(f"запросов сделано            : {parser.count_get_html}")
    print(f"ссылок на очередь парсинга  : {len(parser.links)}")
    print(f"спарсеные ссылки            : {len(parser.cheaking_links)}")
 


        