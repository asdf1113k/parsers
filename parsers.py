# парсер с рекурсивным парсингом ссылок и без него V2

from requests import Response, get

from bs4 import BeautifulSoup
from colorama import init, Fore  # !!! для тестов

init(autoreset=True)  # !!! для тестов


class Parser:
    def __init__(
        self, url: str, recursion_search: bool = False, auto_run=False
    ) -> None:
        self.url: str = self.set_url(url)
        self.html: str = ""
        self.link_queue = []
        self.cheaking_links = set()
        self.count_recursion = 1
        self.count_get_html = 0
        self.recursion_search: bool = recursion_search

        if auto_run:
            self.run()

    def set_url(self, new_url: str) -> str:
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

    def set_auto_run(self, new_value: bool) -> None:
        if type(new_value) is bool:
            self.auto_run: bool = new_value
        else:
            raise ValueError(
                f"в {self.set_auto_run.__name__} передано не bool значение"
            )

    def get_html(self, url) -> None:
        self.count_get_html += 1

        response: Response = get(url, allow_redirects=True)
        if 200 <= response.status_code <= 399:
            if url not in self.cheaking_links:
                print(
                    Fore.BLUE
                    + f"(get_html) ссылка {response.url} добавлена в set провереных"
                )  # !!! для тестов
                self.html: str = response.text
                self.cheaking_links.add(response.url)
        else:
            self.html = "<html></html>"

    def search_links(self) -> None:
        """делает поиск по html page которую присылает get_html()
        если ссылок с нет в проверетых он добавляет их в очередь на парсинг"""
        # !!! можно создать отдельный set в который будут записыватся сторонии ссылки не связвные с переданным url
        # !!! скорее всего лучше сделать получение значения href в переменую и продолжение дальнейших работ
        # потому что, как мне кажется вызывать каждый раз метод для получения значения не логично
        # !!! замерить скорость работы такого кода
        soup = BeautifulSoup(self.html, "lxml")
        for tag in soup.find_all():
            if tag.get("href") is None:
                # print("(search_links): не найдено ") # для тестов !!!
                continue
            if (
                f"{self.url}{tag.get('href')}" not in self.cheaking_links
                and f"{self.url}{tag.get('href')}" not in self.link_queue
            ):
                if tag.get("href").startswith("https://", 0, 8) or tag.get(
                    "href"
                ).startswith("http://", 0, 8):  # type: ignore
                    print(
                        Fore.YELLOW
                        + f"(search_links): ссылка на другой ресурс {tag.get('href')}"
                    )
                    # self.link_queue.append(f"{tag.get('href')}")
                print(
                    Fore.GREEN
                    + f"(search_links): найдена ссылка {self.url}{tag.get('href')}"
                )  # для тестов !!!
                self.link_queue.append(f"{self.url}{tag.get('href')}")

    def is_check_links_in_link_queue(self) -> None:
        """удаляет ссылки которые уже проверены из очереди на парсинг"""
        for link in self.link_queue:
            if link in self.cheaking_links:
                self.link_queue.remove(link)
        # (done) сделать удаление тех ссылок из link_queue которые есть в cheaking_links

    def run(self) -> None:
        self.get_html(self.url)
        self.search_links()
        if not self.recursion_search:
            return

        while len(self.link_queue) > 0:
            if self.count_recursion <= 0:
                return
            self.count_recursion -= 1

            self.is_check_links_in_link_queue()
            # сделать удаление ссылок которые есть в провереныйх, из листа на очередь
            print(
                f"запросов сделано            : {self.count_get_html}"
            )  # для тестов !!!
            print(
                f"ссылок на очередь парсинга  : {len(self.link_queue)}"
            )  # для тестов !!!
            print(f"links :{self.link_queue}")  # для тестов !!!
            print(
                f"спарсеные ссылки            : {len(self.cheaking_links)}"
            )  # для тестов !!!
            print(self.cheaking_links)  # для тестов !!!
            print("-" * 100)  # для тестов !!!

            # не делается поиск ссылок после запроса html
            # ошибка в не внимательности. забыл поставить скобки :/
            recursion_links = self.link_queue
            for link in recursion_links:
                self.get_html(link)
                self.search_links()


if __name__ == "__main__":
    url = "https://wwwww.jodi.org/"
    try:
        parser = Parser(url, auto_run=True, recursion_search=True)
    except KeyboardInterrupt:
        pass
    print(f"запросов GET сделано        : {parser.count_get_html}")
    print(f"ссылок на очередь парсинга  : {len(parser.link_queue)}")
    print(f"спарсеные ссылки            : {len(parser.cheaking_links)}")
