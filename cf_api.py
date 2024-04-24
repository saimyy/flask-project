from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json

from selenium.webdriver.common.by import By


def create_json(find_handle):
    handle = 'flask_poject'
    password = 'flask112233@'
    dict_contest = {}
    driver = webdriver.Chrome()
    driver.get("https://codeforces.com/enter")
    email_input = driver.find_element(By.ID, 'handleOrEmail')
    email_input.clear()
    email_input.send_keys(handle)
    password_input = driver.find_element(By.ID, 'password')
    password_input.clear()
    password_input.send_keys(password)
    time.sleep(3)
    driver.find_element(By.CLASS_NAME, 'submit').click()
    time.sleep(5)
    driver.get("https://codeforces.com/group/Sm8APQqnoi/contests")
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find_all('table')[1]
    rows = table.find_all('tr', class_='highlighted-row')
    for row in rows:
        tds = row.find_all('td')
        name = tds[0].get_text(strip=True)
        f = name.find('Войти')
        name = name[:f]
        han = tds[4]
        link = tds[0].find('a').get('href')
        if find_handle in han.text:
            dict_contest[name] = link
    with open(f'json/{find_handle}_contest.json', 'w') as fp:
        json.dump(dict_contest, fp, indent=4)
    driver.close()
    driver.quit()
