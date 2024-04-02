import requests
from bs4 import BeautifulSoup

session = requests.Session()
k = session.post('https://codeforces.com/enter', {
    'handleOrEmail': 'chshiev07@mail.ru',
    'password': 'Slava2007@'})
print(k)