from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json
import xlsxwriter
import random
from selenium.webdriver.common.by import By


def new_excel_table(submit, han):
    result_array = []
    handle = 'flask_poject'
    password = 'flask112233@'
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
    for item in submit:
        excel_array = []
        driver.get(item[1])
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find_all('table')[0]
        rows = table.find_all('tr')[1:-1]
        for row in rows:
            tds = row.find_all('td')
            nick = tds[1].get_text(strip=True)
            cnt = int(tds[2].text)
            print(cnt)
            flag = False
            flag1 = False
            if '*' not in nick:
                excel_array.append([nick, cnt, 0])
            else:
                for i in excel_array:
                    if i[0] == nick.lstrip('* '):
                        flag = True
                        i[2] += cnt
                        break
                if not flag:
                    excel_array.append([nick.lstrip('* '), 0, cnt])
        result_array.append(excel_array)
    p = f'{han}{random.randint(1, 10000)}_standings.xlsx'
    workbook = xlsxwriter.Workbook(p)
    worksheet = workbook.add_worksheet('1')
    worksheet.write(0, 0, 'Участник')
    j = 1
    x, y = 2, 1
    for i in submit:
        worksheet.write(0, j, i[0])
        worksheet.write(1, j, 'контест')
        worksheet.write(1, j + 1, 'дорешка')
        j += 2
    tmp = {}
    for item in result_array:
        for arr in item:
            if arr[0] not in tmp:
                worksheet.write(x, 0, arr[0])
                tmp[arr[0]] = x
                worksheet.write(x, y, arr[1])
                worksheet.write(x, y + 1, arr[2])
                x += 1
            else:
                worksheet.write(tmp[arr[0]], y, arr[1])
                worksheet.write(tmp[arr[0]], y + 1, arr[2])
        y += 2
    workbook.close()
    return p