import requests
from hyper.contrib import HTTP20Adapter
from fake_useragent import UserAgent

ua = UserAgent(use_cache_server=False)

s = requests.Session()
s.mount('https://', HTTP20Adapter())
r = s.get('https://www.avito.ru/web/1/items/phone/2471365057', headers={
    'User-Agent': ua.random
},
          proxies={'https': '176.192.70.58'})
print(r.status_code)

with open('./response1.html', mode='w', encoding='UTF-8') as file:
    file.write(r.text)
