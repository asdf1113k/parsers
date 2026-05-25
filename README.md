# [ParserLinks.py](ParserLinks.py)
## сделать

отдельный set для записи стороних ссылок а то они просто логируются

запрос страницы html с использованием selenium

функцию links возвращаемую ссылки

дописать ParserClass

## идея 
сделать такой синтаксис для вызова класса
```
from parsers import ParserLinks
    url = "https://google.com"
    ParserLinks(url, recursiv_search=True)
    print(ParserLinks.links()) # вывод список с ссылками
```
+ `+` не надо вызывать метод ParserLinks.run() сразу получаешь ссылки

