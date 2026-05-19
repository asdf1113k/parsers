"""узнавал назване объектов возвращаемые либой requests"""

import requests as rq

responce = rq.get("https://google.com")
print(type(responce))  # <class 'requests.models.Response'>
