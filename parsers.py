# парсер с рекурсивным парсингом ссылок и без него V2

# !!! не запутан ли код? распутываю

from requests import Response, get

from time import sleep, time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from colorama import init, Fore  

init(autoreset=True)


class Parser:
    def __init__(
        self, url: str, auto_run: bool = True, selenium: bool = False
    ) -> None:
        self.url: str = self.__set_url(url)
        self.html: str = ""
        self.count_get_html = 0
        self.auto_run = self.__set_auto_run(auto_run)
        self.log = ''

    def __set_url(self, new_url: str) -> str:
        if (
            new_url.startswith("https://", 0, 8)
            or new_url.startswith("http://", 0, 8)
            and new_url[-1] == "/"
        ):
            return new_url
        else:
            raise ValueError(
                f"переданный url({new_url}) не соответствует качествам url. пример как должен выглядеть url (https://site.com/)"
            )

    def __set_auto_run(self, new_value: bool) -> bool:
        if type(new_value) is bool:
            return new_value
        else:
            raise ValueError(
                f"в '{self.set_auto_run.__name__}' передано не bool значение \n переданое значение {new_value}"
            )



    def get_html(self, url) -> str:
        self.count_get_html += 1
        response: Response = get(url, allow_redirects=True)
        
        if 200 <= response.status_code <= 399:
            self.entry_in_the_logs(
                Fore.BLUE +
                f"(get_html) удачный ответ от сервера - '{response.status_code}'")

            self.html: str = response.text
            return self.html
                
        else:
            self.entry_in_the_logs(
                    Fore.RED +
                    f"(get_html) НЕ удачный ответ от сервера - '{response.status_code}'"
                    )
                
            self.html = "<html></html>"
            return self.html
        
    def entry_in_the_logs(self, new_entry: str = '' ):
        """добавляет новую запись в логи
        пример записи - '(название функции экземпляра) событие которое произошло в экземпляре класса'"""

        if type(new_entry) is str:
            self.log += new_entry + ' \n'
        


    def get_html_selenium(self, url: str, pause: int = 10):
        """запрос html страницы с использованием selenium
        url - url адрес запрашиваемой страницы
        pause - время требующееся для для работы js
        комент от разраба - не пользовался selenium всё что связано
        с selenium написала нейронка"""
        options = Options()
        options.add_argument("--headless")  # без GUI
        driver = webdriver.Chrome(options=options)

        driver.get(self.url)
        sleep(pause)
        self.html = driver.page_source  # уже с выполненным JS
        driver.quit()



class ParserLinks(Parser):
    """"минусы парсит только значения с атрибута href всех тегов"""
    def __init__(
        self, url: str, auto_run: bool = True, recursion_search: bool = False
    ) -> None:

        super().__init__(url, auto_run=auto_run)
        self.__link_queue = []
        self.__cheaking_links = set()
        self.__links_included_in_get_html = set()
        self.external_links = set() # 'external' переводится как 'внешние'
        self.recursion_search: bool = recursion_search

        if self.auto_run:
            self.run()
    
    def get_html(self, url) -> None:
        self.count_get_html += 1
        self.__remove_url_from_queue(url)
        # вот делается удаление, потом в очередь опять добавляются ссылки в search_links
        response: Response = get(url, allow_redirects=True)
        
    
        if 200 <= response.status_code <= 399:
            if url not in self.__cheaking_links:

                self.entry_in_the_logs(
                    Fore.BLUE +
                    f"(get_html) ссылка {response.url} добавлена в set провереных"
                )

                self.html: str = response.text
                self.__cheaking_links.add(response.url)
        else:
            self.html = "<html></html>"

    def search_links(self) -> None:
        """делает поиск ссылок по html page которую присылает 'get_html()'
        и добавляет новые ссылки в очередь на парсинг"""
        # !!! можно создать отдельный set в который будут записыватся сторонии ссылки не связвные с переданным url
        # !!! скорее всего лучше сделать получение значения href в переменую и продолжение дальнейших работ
        # потому что, как мне кажется вызывать каждый раз метод для получения значения не логично
        # !!! замерить скорость работы такого кода
        
        soup = BeautifulSoup(self.html, "lxml")
        for tag in soup.find_all():
            value_href = tag.get("href")
            # !!! протестить скорость работы
            # заменить value_href на tag.get("href") 
            # и замерить скорость работы

            if value_href is None:
                continue

            if (
                value_href.startswith("https://", 0, 8) # type: ignore
                or value_href.startswith("http://", 0, 8)  # type: ignore
                ): 
                self.entry_in_the_logs(
                Fore.YELLOW +
                f"({self}.{self.search_links.__name__}): найдена ссылка на другой ресурс {value_href}",
                )

                

            if (
                f"{self.url}{value_href}" not in self.__cheaking_links
                and f"{self.url}{value_href}" not in self.__links_included_in_get_html
                and f"{self.url}{value_href}" not in self.__link_queue
            ):
                self.entry_in_the_logs(
                Fore.GREEN +
                f"(search_links): найдена ссылка {self.url}{value_href}",
                )

                self.__link_queue.append(f"{self.url}{value_href}")

    def __remove_url_from_queue(self, url) -> None:
        """удаляет ссылки, которые уже проверены, из очереди на парсинг"""

        if url in self.__link_queue:
            self.__link_queue.remove(url)
        
        self.__links_included_in_get_html.add(url)
        # (done) сделать удаление тех ссылок из link_queue которые есть в cheaking_links

    def run(self) -> None:
        self.get_html(self.url)
        self.search_links()
        if not self.recursion_search:
            return

        while len(self.__link_queue) > 0:

            self.entry_in_the_logs(
                f"запросов сделано            : {self.count_get_html}"
            )

            self.entry_in_the_logs(
                f"ссылок на очередь парсинга  : {len(self.__link_queue)}"
            )

            self.entry_in_the_logs(f"links :{self.__link_queue}")

            self.entry_in_the_logs(f"спарсеные ссылки            : {len(self.__cheaking_links)}")
            
        
            
    
            recursion_links = self.__link_queue
            for link in recursion_links:
                self.get_html(link)
                self.search_links()
                # self.is_check_links_in_link_queue()
                # не сработает его надо ставить в get_html


class ParserClasses(Parser):
    def __init__(self, url: str):
        self.url = url
        self.html = self.get_html()
        self.classes = set()

    def get_html(self):
        options = Options()
        options.add_argument("--headless")  # без GUI
        driver = webdriver.Chrome(options=options)

        driver.get(self.url)
        sleep(10)
        html = driver.page_source  # уже с выполненным JS
        driver.quit()
        return html

    def search_classes(self):
        soup = BeautifulSoup(self.html, "lxml")
        soup.find_all("")

    def run(self):

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


if __name__ == "__main__":
    url = "https://wwwww.jodi.org/"
    url1 = "https://stepik.org/"
    start = time()
    try:
        parser = ParserLinks(url, recursion_search=True)
        parser.get_html(parser.url)
    except KeyboardInterrupt:
        pass
    # print(dir(parser))
    print(parser.log)
    parser.recursion_search
    end = time()
    print(f"'ParserLinks' время работы: {end - start}")

    # print(f"запросов GET сделано        : {parser.count_get_html}")
    # print(f"ссылки попавшме в get_html  : {parser._ParserLinks__links_included_in_get_html}")
    # print(f"ссылок на очередь парсинга  : {len(parser._ParserLinks__link_queue)}")
    # print(f"спарсеные ссылки            : {len(parser._ParserLinks__cheaking_links)}")
