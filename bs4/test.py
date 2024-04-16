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
driver.find_element(By.CLASS_NAME, 'submit').click()
driver.get("https://codeforces.com/group/Sm8APQqnoi/contests")
time.sleep(5)
