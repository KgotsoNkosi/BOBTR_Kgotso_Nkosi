import requests

r = requests.get('https://titanic.businessoptics.biz/survival/')
print(r.json())