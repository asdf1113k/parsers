# парсер ссылок с домена wwwww.jodi.org

import requests as rq
from bs4 import BeautifulSoup


def collection_links(domain, url_path=""):
    """сбор ссылок с переданной страницы"""
    responce = rq.get(domain + url_path)
    soup = BeautifulSoup(responce.text, "lxml")

    result = [domain + url_path]
    all_links = soup.find_all("a")
    for link in all_links:
        result.append(link.get("href"))
    return result


#
# with open("wwwww.jodi.org.txt", "w", newline="") as file_with_links:
#     for link in links:
#         file_with_links.write(link + "\n")


def open_links(links: list[str]) -> None:
    paths = []
    for link in links[1:-1]:
        paths.append(rq.get(links[0] + link))
    return paths


def main():
    domain = "https://wwwww.jodi.org/"
    print(open_links(collection_links(domain)))
    for i in open_links(collection_links(domain)):
        print(i.url)



if __name__ == "__main__":
    main()

    # url_paths_list = []
    #
    # result = []
    # domain = "https://wwwww.jodi.org/"
    # for link in Collection_links(domain):
    #     url_paths_list.append(link)
    # else:
    #     result.append(url_paths_list)
    #
    #
    # for url_path in set(url_paths_list):
    #     for link in Collection_links(domain, url_path):
    #         result.append(link)
    #
    # print(result)
