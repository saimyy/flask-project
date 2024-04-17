from bs4 import BeautifulSoup
from selenium import webdriver
import time

from selenium.webdriver.common.by import By

handle = 'saimyy_'
password = 'Slava2007@'
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
k = soup.find_all('table')[5]
print(k)
